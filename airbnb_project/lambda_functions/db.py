"""
Main file to create connection to the database
"""
import os
from typing import Optional

import pymongo

password: Optional[str] = os.environ.get("MONGO_PASSWORD")
doc_db_url: str = os.environ.get(
    "DOC_DB_URL", "main-airbnb-docdb.cluster-capqutxquohy.eu-west-1.docdb.amazonaws.com"
)
connection_params: str = os.environ.get(
    "CONNECTION_PARAMS",
    '?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"',
)
connection_url: str = (
    f"mongodb://docdb:{password}@{doc_db_url}:27017/{connection_params}"
)

if os.getenv("DOC_DB_URL"):
    client: pymongo.MongoClient = pymongo.MongoClient(connection_url)
elif os.getenv("IS_LOCALSTACK"):
    client: pymongo.MongoClient = pymongo.MongoClient(
        host="docker.internal.host", port=27017
    )
else:
    client: pymongo.MongoClient = pymongo.MongoClient()
