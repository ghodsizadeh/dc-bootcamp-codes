"""
Utility functions
- check_dates_available
"""
from typing import Dict, Sequence


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
