import json
import unittest
import os
import sys

# Add the parent directory (containing 'api') to the Python path
from datetime import datetime
from unittest.mock import patch, Mock

parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(parent_dir, '..'))

from api.app import validate_input_params, prepare_response, create_query
from api.models import AnalyticsRequest, Granularity


class TestApp(unittest.TestCase):

    def test_validate_input_params_valid(self):
        # Valid input parameters
        request_args = {
            'groupBy': 'attribute1,attribute2',
            'filters': [{'attribute': 'attribute3', 'value': 42}],
            'startDate': '2023-01-01T08:00:00',
            'endDate': '2023-01-05T08:00:00',
            'granularity': 'hourly',
            'metrics': 'metric1,metric2'
        }

        result, error = validate_input_params(request_args)
        print(f"Result: {result}, Error: {error}")

        # Updated assertion
        assert result is not None, f"Validation failed. Error: {error}"

    def test_validate_input_params_validation_error(self):
        # Validation error in input parameters
        request_args = {
            'groupBy': 'attribute1,attribute2',
            'filters': [{'attribute': 'attribute3', 'value': 'invalid_value'}],
            'startDate': '2022-01-01',
            'endDate': '2022-01-31',
            'granularity': 'hourly'
        }

        result, error = validate_input_params(request_args)
        print(f"Error: {error}")
        assert result is None
        assert error is not None
        assert '3 validation errors for AnalyticsRequest' in error['error']
        assert 'field required (type=value_error.missing)' in error['error']
        assert 'invalid datetime format (type=value_error.datetime)' in error['error']

    def test_validate_input_params_invalid_groupby(self):
        # Invalid groupBy attribute
        request_args = {
            'groupBy': 'invalid_attribute',
            'filters': [{'attribute': 'attribute3', 'value': 42}],
            'startDate': '2023-01-01T08:00:00',
            'endDate': '2023-01-05T08:00:00',
            'granularity': 'hourly',
            'metrics': 'metric1,metric2'  # Add metrics field
        }

        result, error = validate_input_params(request_args)
        print(f"Error: {error}")

        # Updated assertion to match the raised ValueError message
        assert result is None
        assert error is not None
        assert 'Invalid attributes: invalid_attribute' in error['error']

    @patch('api.app.Session')
    def test_create_query_hourly_granularity(self, mock_session):
        # Test creating a query with hourly granularity
        request_data = AnalyticsRequest(
            groupBy='event_date',
            metrics='metric1,metric2',  # Add this line to include the 'metrics' field
            granularity=Granularity.hourly,
            filters=[],
            startDate='2023-01-01T08:00:00',
            endDate='2023-01-05T08:00:00'
        )

        # Mock the session and query
        mock_query = Mock()
        mock_session.return_value.query.return_value = mock_query
        mock_session.return_value.__enter__.return_value = mock_session.return_value

        # Call the create_query function
        query, error_response = create_query(mock_session, request_data)

        # Assertions
        assert error_response is None
        assert query is not None

        # Inspect the generated SQL query without executing it
        generated_sql = str(mock_query)
        # Assertions
        assert error_response is None
        assert query is not None

    def test_prepare_response_empty_results(self):
        # Test preparing response with empty results
        result = prepare_response([])
        expected_response = []
        self.assertEqual(result, expected_response)

    def test_prepare_response_single_result(self):
        # Test preparing response with a single result
        mock_result = Mock()
        mock_result._fields = ['date', 'metric1', 'metric2']
        setattr(mock_result, 'date', datetime(2023, 1, 1))
        setattr(mock_result, 'metric1', 10)
        setattr(mock_result, 'metric2', 5.5)

        result = prepare_response([mock_result])
        expected_response = {
            'results': [
                {
                    'date': datetime(2023, 1, 1, 0, 0).isoformat(),
                    'metric1': 10,
                    'metric2': 5.5
                }
            ]
        }

        # Convert to dictionaries
        actual_dict = json.loads(result)
        expected_dict = expected_response

        # Assert the dictionaries
        self.assertDictEqual(actual_dict, expected_dict)

    def test_prepare_response_multiple_results(self):
        # Test preparing response with multiple results
        mock_result1 = Mock()
        mock_result1._fields = ['date', 'metric1', 'metric2']
        setattr(mock_result1, 'date', datetime(2023, 1, 1))
        setattr(mock_result1, 'metric1', 10)
        setattr(mock_result1, 'metric2', 5.5)

        mock_result2 = Mock()
        mock_result2._fields = ['date', 'metric1', 'metric2']
        setattr(mock_result2, 'date', datetime(2023, 1, 2))
        setattr(mock_result2, 'metric1', 15)
        setattr(mock_result2, 'metric2', 7.5)

        result = prepare_response([mock_result1, mock_result2])
        expected_response = {'results': [
            {'date': datetime(2023, 1, 1).isoformat(), 'metric1': 10, 'metric2': 5.5},
            {'date': datetime(2023, 1, 2).isoformat(), 'metric1': 15, 'metric2': 7.5}
        ]}
        self.assertEqual(json.loads(result), expected_response)


if __name__ == "__main__":
    unittest.main()
