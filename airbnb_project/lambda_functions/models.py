"""
Data Models for the Airbnb Project
"""
from typing import Any, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel


class Host(BaseModel):
    """Host Model"""

    host_id: Union[int, UUID]
    host_name: str


class Calendar(BaseModel):
    """Calendar Model"""

    date: str
    price: float
    adjusted_price: float
    availability: bool


class Room(BaseModel):
    """Room Model"""

    _id: Optional[Any]
    name: str
    neighborhood: str
    latitude: float
    longitude: float
    room_type: str
    minimum_nights: int
    number_of_reviews: int
    last_review: str
    reviews_per_month: int
    calculated_host_listings_count: int
    number_of_reviews_ltm: int
    availability_365: int
    license: str
    host: Host
    calendar: List[Calendar]


class User(BaseModel):
    """User Model"""

    name: str
    email: str
    phone: str
    bearer_token: str


#############
# Body, Response and Headers
#############


class QueryFunctionQueryStringParameters(BaseModel):
    """Query String Parameters for the Query Function"""

    check_in: Optional[str]
    check_out: Optional[str]
    area: Optional[str]


class QueryEvent(BaseModel):
    """Event for the Query Function"""

    queryStringParameters: QueryFunctionQueryStringParameters = (
        QueryFunctionQueryStringParameters()
    )


class QueryResponse(BaseModel):
    """Response for the Query Function"""

    body: List[Room]
    statusCode: int


class BookingBody(BaseModel):
    """Body for the Booking Function"""

    check_in: str
    check_out: str
    area: str
