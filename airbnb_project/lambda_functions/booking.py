"""
Lambda function that check if a calendar booking is valid
and send request to SQS to book the room
in main database
"""
import os
from datetime import datetime
from typing import Dict, Sequence

import boto3

from db import client


def check_dates_available(room_id: str, check_in: str, check_out: str):
    """
    Check if all the dates are available in the room calendar
    """
    collection = client.airbnb.listings
    aggregate_pipeline: Sequence[Dict] = [
        {"$match": {"_id": room_id}},
        {"$unwind": "$calendar"},
        {
            "$match": {
                "calendar.date": {"$gte": check_in, "$lte": check_out},
                "calendar.availability": {"$eq": False},
            },
        },
        {"$group": {"_id": "$_id", "calendar": {"$push": "$calendar"}}},
    ]
    return list(collection.aggregate(aggregate_pipeline))


def authorize_user(bearer_token: str):
    """
    Check if the user is authorized
    """
    user_collection = client.airbnb.users
    return user_collection.find_one({"bearer_token": bearer_token})


# pylint: disable=unused-argument,too-many-locals
def lambda_handler(event, context):
    """
    Get Check in and Check out dates from the event
    and send request to SQS to book the room

    """
    # Get the check in and check out dates from the event
    headers = event.get("headers", {})
    bearer_token = headers.get("Authorization")
    if bearer_token is None:
        return {"statusCode": 401, "body": "Unauthorized"}
    bearer_token = bearer_token.split(" ")[1]
    user = authorize_user(bearer_token)
    if user is None:
        return {"statusCode": 401, "body": "Unauthorized"}

    body = event.get("body", {})
    check_in = body.get("check_in")
    check_out = body.get("check_out")
    room_id = body.get("room")

    if not check_in or not check_out or not room_id:
        return {"statusCode": 400, "body": "Missing required parameters"}
    collection = client.airbnb.listings
    room = collection.find_one({"_id": room_id})

    if not room:
        return {"statusCode": 404, "body": "Room not found"}

    # check if all the dates are available in the room calendar
    if check_dates_available(room_id, check_in, check_out):

        return {"statusCode": 400, "body": "Dates are not available"}

    # check if the check in and check out dates are valid and available
    # Send request to SQS to book the room
    endpoint_url = (
        None
        if os.getenv("AWS_SESSION_TOKEN")
        else "https://localhost.localstack.cloud:4566"
    )
    sqs = boto3.resource("sqs", endpoint_url=endpoint_url)

    booking_queue_name = os.environ.get("BOOKING_QUEUE_NAME", "booking-queue")
    try:
        queue = sqs.get_queue_by_name(QueueName="booking_queue_name")
    # pylint: disable=bare-except
    except:
        queue = sqs.create_queue(QueueName="booking_queue_name")

    # if the queue is FIFO add  GroupId and MessageDeduplicationId
    if ".fifo" in booking_queue_name:
        response = queue.send_message(
            MessageBody=f"{check_in}:{check_out}:{room}",
            MessageGroupId="Booking",
            MessageDeduplicationId=f"{check_in}:{check_out}"
            f":{room_id}:{user}:{datetime.now().timestamp()}",
        )
    else:
        response = queue.send_message(
            MessageBody=f"{check_in}:{check_out}:{room}",
        )

    return {
        "statusCode": 202,
        "body": "Booking request is in progress",
        "response": response,
    }
