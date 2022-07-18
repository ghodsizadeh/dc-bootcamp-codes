"""
Test functionality of query lambda functions with following tests
1. Health check and testing with no query parameters
2. Testing with query parameters with area
3. Testing with query parameters with check in and check out
4. Testing with query parameters with check in and check out with no rooms
"""
# pylint: disable=unused-argument

from typing import Dict

from models import Booking, BookingMessage, UpdateDBEvent
from update_db import lambda_handler


def test_update_db(update_db_event: UpdateDBEvent, bookings_collection):
    """
    Test if function works with one room in the database
    """
    event = update_db_event.dict()

    context: Dict = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200
    body = response["body"]
    assert body == "OK"

    # check if the room is booked in the database
    record = BookingMessage.from_message(update_db_event.Records[0].body)
    booking = Booking(**bookings_collection.find_one({"room_id": record.room_id}))
    assert booking.room_id == record.room_id
    assert booking.check_in == record.check_in
    assert booking.check_out == record.check_out
