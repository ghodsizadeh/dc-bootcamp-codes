"""
Lambda function that check if a calendar booking is valid
and send request to SQS to book the room
in main database
"""
import os
from datetime import datetime

import boto3
import pymongo

password = os.environ.get("MONGO_PASSWORD")
doc_db_url = os.environ.get(
    "DOC_DB_URL", "main-airbnb-docdb.cluster-capqutxquohy.eu-west-1.docdb.amazonaws.com"
)
connection_params = os.environ.get(
    "CONNECTION_PARAMS",
    '?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"',
)
connection_url = f"mongodb://docdb:{password}@{doc_db_url}:27017/{connection_params}"

client = pymongo.MongoClient()


def check_dates_available(room_id: "str", check_in: str, check_out: str):
    """
    Check if all the dates are available in the room calendar
    """
    collection = client.airbnb.listings
    aggregate_query = [
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
    res = list(collection.aggregate(aggregate_query))
    return list(res)


# pylint: disable=unused-argument
def lambda_handler(event, context):
    """
    Get Check in and Check out dates from the event
    and send request to SQS to book the room

    """
    # Get the check in and check out dates from the event
    body = event.get("body", {})
    check_in = body.get("check_in", "")
    check_out = body.get("check_out", "")
    room_id = body.get("room", "")

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
    if ".fifo" in booking_queue_name:
        response = queue.send_message(
            MessageBody=f"{check_in}:{check_out}:{room}",
            MessageGroupId="Booking",
            MessageDeduplicationId=f"{check_in}:{check_out}:{room_id}:{datetime.now().timestamp()}",
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
