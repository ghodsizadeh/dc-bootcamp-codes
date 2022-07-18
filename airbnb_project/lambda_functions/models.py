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


class Booking(BaseModel):
    """
    Booking Model
    """

    user_id: str
    room_id: str
    check_in: str
    check_out: str
    total_cost: float
    message_body: str


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


class BookingMessage(BaseModel):
    """for use in message decoder to get
    check_in, check_out, room_id, user_id, ts"""

    check_in: str
    check_out: str
    room_id: str
    user_id: str
    ts: str

    @classmethod
    def from_message(cls, message: str) -> "BookingMessage":
        """
        Decode the message
        """
        check_in, check_out, room_id, user_id, ts = message.split(":")
        return BookingMessage(
            check_in=check_in,
            check_out=check_out,
            room_id=room_id,
            user_id=user_id,
            ts=ts,
        )

    def get_message_str(self):
        """
        Get message string like it was in queue
        """
        return (
            f"{self.check_in}:{self.check_out}:{self.room_id}:{self.user_id}:{self.ts}"
        )


class SQSMessage(BaseModel):
    """SQS Message for the Booking Function"""

    body: str
    messageId: str
    receiptHandle: str
    attributes: dict
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str


class UpdateDBEvent(BaseModel):
    """Event for the Update DB Function"""

    Records: List[SQSMessage]
