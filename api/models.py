from datetime import datetime, date
from enum import Enum
from typing import List
from typing import Union, Optional

from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'schema': 'test'}  # Specify the schema name

    id = Column(Integer, primary_key=True)
    event_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    attribute1 = Column(Integer)
    attribute2 = Column(Integer)
    attribute3 = Column(Integer)
    attribute4 = Column(String(255))
    attribute5 = Column(String(255))
    attribute6 = Column(Boolean)
    metric1 = Column(Integer, nullable=False)
    metric2 = Column(Numeric(10, 2), nullable=False)


# Define Pydantic model for event creation request
class EventCreate(BaseModel):
    id: int
    event_date: datetime
    attribute1: int
    attribute2: int
    attribute3: int
    attribute4: str
    attribute5: str
    attribute6: bool
    metric1: int
    metric2: float


class Granularity(str, Enum):
    hourly = 'hourly'
    daily = 'daily'


class AnalyticsRequest(BaseModel):
    groupBy: str
    filters: Optional[List[dict]] = []
    metrics: str
    granularity: Granularity
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None


class AnalyticsResponseItem(BaseModel):
    date: Union[datetime, date]
    metric1: int
    metric2: float
    attribute1: Optional[int] = None
    attribute2: Optional[int] = None
    attribute3: Optional[int] = None
    attribute4: Optional[str] = None
    attribute5: Optional[str] = None
    attribute6: Optional[bool] = None

    @validator("date", pre=True, always=True)
    def convert_date_to_datetime(cls, value):
        if isinstance(value, date):
            # If it's a date, convert it to a datetime with midnight as the time
            return datetime.combine(value, datetime.min.time())
        return value


class AnalyticsResponse(BaseModel):
    results: list[AnalyticsResponseItem]
