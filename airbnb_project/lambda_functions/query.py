"""
Lambda function that connects to DocumentDB
and returns a list of available rooms in the given {area}
from {check in date} to {check out date}
with availability = True
"""
import os

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
try:
    client = pymongo.MongoClient()
except Exception as e:
    print(e)
    raise e

# pylint: disable=unused-argument
def lambda_handler(event, context) -> dict:
    """
    return list of available rooms
    in the given {area}
    from {check in date} to {check out date}"""
    listing = client.airbnb.listings
    query_params = event.get("queryStringParameters", {})
    area = query_params.get("area")
    check_in = query_params.get("check_in")
    check_out = query_params.get("check_out")
    query = {}
    aggregate_query = []
    if area:
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
            {"$group": {"_id": "$_id", "calendar": {"$push": "$calendar"}}},
        ]
        rooms_list = listing.aggregate(aggregate_query)
    else:
        rooms_list = listing.find(query)

    return {"statusCode": 200, "body": list(rooms_list)}
