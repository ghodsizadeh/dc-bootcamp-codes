"""
Lambda function that invoked by a SQS queue
and update the original room document in the database
and create booking document in the database
"""

import datetime
import logging

from bson.objectid import ObjectId

from db import client
from models import Booking, BookingMessage, SQSMessage, UpdateDBEvent
from utils import check_dates_available

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def update_booking_record(message: SQSMessage) -> bool:
    """Update each record"""
    booking_message = BookingMessage.from_message(message.body)
    # check_in, check_out, room_id, user_id, _ = message_body.split(":")

    bookings = client.airbnb.bookings
    if bookings.find_one({"message_body": message.body}):
        logger.info(f"Booking already processed: {message.body}")
        return False
    if check_dates_available(
        booking_message.room_id, booking_message.check_in, booking_message.check_out
    ):
        logger.info(f"Dates are not available: {message.body}")
        return False
    listings = client.airbnb.listings
    total_cost = listings.aggregate(
        [
            {"$match": {"_id": ObjectId(booking_message.room_id)}},
            {"$unwind": "$calendar"},
            {
                "$match": {
                    "calendar.date": {
                        "$gte": booking_message.check_in,
                        "$lte": booking_message.check_out,
                    }
                }
            },
            {"$group": {"_id": "$_id", "total_cost": {"$sum": "$calendar.price"}}},
        ]
    )

    total_cost = next(total_cost)["total_cost"]
    # booking = Booking(
    #     user_id=user_id,
    #     room_id=room_id,
    #     check_in=check_in,
    #     check_out=check_out,
    #     total_cost=total_cost,
    #     message_body=message_body,
    # )
    booking = Booking(
        user_id=booking_message.user_id,
        room_id=booking_message.room_id,
        check_in=booking_message.check_in,
        check_out=booking_message.check_out,
        total_cost=total_cost,
        message_body=booking_message.get_message_str(),
    )
    # bookings.insert_one(booking.dict())

    bookings.insert_one(booking.dict())

    # make room unavailable for the days between check_in and check_out
    # check_in = 2021-01-01
    check_in_date = datetime.datetime.strptime(booking_message.check_in, "%Y-%m-%d")
    check_out_date = datetime.datetime.strptime(booking_message.check_out, "%Y-%m-%d")
    # update all at the same time

    # update all subdocuments with date between check_in and check_out availablity to False

    for i in range(int((check_out_date - check_in_date).days)):
        date = (check_in_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        listings.update_one(
            {"_id": ObjectId(booking_message.room_id), "calendar.date": date},
            {"$set": {"calendar.$.availability": False}},
        )
    logger.info(f"Booking processed: {booking_message.get_message_str()}")

    return True


# pylint: disable=unused-argument
def lambda_handler(event: dict, context: dict) -> dict:
    """
    Get the records from the SQS queue
    and update the original room document in the database
    and create booking document in the database
    if the request is valid
    and not processed yet"""

    event_data = UpdateDBEvent(**event)
    if event_data.Records is None:
        return {"statusCode": 400, "body": "Missing required parameters"}
    records = event_data.Records
    for message in records:
        update_booking_record(message)
    return {"statusCode": 200, "body": "OK"}
