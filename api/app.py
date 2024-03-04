from flask import Flask, request, jsonify
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import AnalyticsRequest, AnalyticsResponse, AnalyticsResponseItem, Granularity, Event, EventCreate

app = Flask(__name__)

engine = create_engine('postgresql://myuser:mypassword@database:5432/mydb')
Session = sessionmaker(bind=engine)


def validate_input_params(request_args):
    try:
        request_data = AnalyticsRequest(**request_args)

        valid_attributes = [attr for attr in dir(Event)]

        invalid_attributes = set(request_data.groupBy.split(",")) - set(valid_attributes)
        if invalid_attributes:
            raise ValueError(f"Invalid attributes: {', '.join(invalid_attributes)}")

        return request_data, None
    except ValidationError as e:
        return None, {"error": str(e)}
    except ValueError as e:
        return None, {"error": str(e)}


def create_query(session, request_data):
    group_by_attributes = []

    if request_data.granularity == Granularity.hourly:
        group_by_attributes.append(func.date_trunc('hour', Event.event_date).label("date"))
    elif request_data.granularity == Granularity.daily:
        group_by_attributes.append(func.date(Event.event_date).label("date"))
    else:
        return None, {"error": "granularity should be specified correctly"}

    group_by_attributes.extend([getattr(Event, attribute) for attribute in request_data.groupBy.split(",")])

    query = (
        session.query(
            *group_by_attributes,
            func.sum(Event.metric1).label('total_metric1'),
            func.sum(Event.metric2).label('total_metric2'),
        )
        .group_by(*group_by_attributes)
    )

    for filter_item in request_data.filters:
        filter_dict = dict(filter_item)
        query = query.filter(getattr(Event, filter_dict['attribute']) == filter_dict['value'])

    if request_data.startDate:
        query = query.filter(Event.event_date >= request_data.startDate)
    if request_data.endDate:
        query = query.filter(Event.event_date <= request_data.endDate)

    return query, None


def prepare_response(results):
    if not results:
        return []

    # Get field names from the first result
    field_names = results[0]._fields if results else []

    response_items = []
    for result in results:
        response_item_data = {field.replace('total_', ''): getattr(result, field) for field in field_names}
        response_item = AnalyticsResponseItem(**response_item_data)
        response_items.append(response_item)

    return AnalyticsResponse(results=response_items).json(by_alias=True, exclude_unset=True, exclude_none=True,
                                                          indent=2)


@app.route('/analytics/query', methods=['GET'])
def get_analytics_data():
    request_data, error_response = validate_input_params(request.args)
    if error_response:
        return jsonify(error_response), 400  # Bad Request

    with Session() as session:
        query, error_response = create_query(session, request_data)
        if error_response:
            return jsonify(error_response), 400  # Bad Request

        results = query.all()

        return prepare_response(results)


@app.route('/event', methods=['POST'])
def add_event():
    try:
        request_data = EventCreate(**request.json)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400  # Bad Request

    new_event = Event(**request_data.dict())

    with Session() as session:
        try:
            session.add(new_event)
            session.commit()
            return jsonify({"message": "Event added successfully"}), 200
        except IntegrityError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
