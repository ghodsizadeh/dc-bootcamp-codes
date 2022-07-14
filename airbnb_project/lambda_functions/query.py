"""
Lambda function that connects to DocumentDB
and returns a list of available rooms in the given {area}
from {check in date} to {check out date}
with availability = True
"""

from typing import Any, Dict, List, Union

import pymongo

from db import client
from models import QueryEvent, QueryResponse, Room


# pylint: disable=unused-argument
def lambda_handler(event: dict, context: dict) -> dict:
    """
    return list of available rooms
    in the given {area}
    from {check in date} to {check out date}"""

    event_body: QueryEvent = QueryEvent(**event)

    listing = client.airbnb.listings
    query_params = event_body.queryStringParameters
    check_in = query_params.check_in
    check_out = query_params.check_out
    query: Dict[str, Any] = {}
    aggregate_query: List[Dict] = []
    if area := query_params.area:
        query["neighborhood"] = area
    if check_in and check_out:
        query["calendar.date"] = {"$gte": check_in, "$lte": check_out}
        # check availability of rooms in the given {area} from {check in date} to {check out date}
        aggregate_query = [
            {"$match": query},
            {"$unwind": "$calendar"},
            {
                "$match": {
                    "calendar.date": {"$gte": check_in, "$lte": check_out},
                    "calendar.availability": {"$eq": True},
                },
            },
            {
                "$group": {
                    "_id": "$_id",
                    "room": {"$first": "$$ROOT"},
                    "calendar": {"$push": "$calendar"},
                }
            },
            {
                "$replaceRoot": {
                    "newRoot": {"$mergeObjects": ["$room", {"calendar": "$calendar"}]}
                }
            },
        ]
        rooms_list: Union[
            pymongo.command_cursor.CommandCursor[Any], pymongo.cursor.Cursor[Any]
        ] = listing.aggregate(aggregate_query)
    else:
        rooms_list = listing.find(query)
    result: List[Room] = [Room(**room) for room in rooms_list]

    response = QueryResponse(body=result, statusCode=200)
    return response.dict()
