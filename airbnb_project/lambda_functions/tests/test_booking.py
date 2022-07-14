"""
Test functionality of booking lambda functions with following tests
1. Health check and testing with one room in the database
2. Testing with one room in the database and not available dates
3. Testing with one room in the database and wrong room id
4. Testing with not authorized user


"""
# pylint: disable=unused-argument

from typing import Dict
from booking import lambda_handler


def test_booking(listings_collection_one_room, users_collection, default_headers):
    """
    Test if function works with one room in the database
    """
    sample_room = listings_collection_one_room.find()[0]
    event = {
        "body": {
            "room": sample_room["_id"],
            "check_in": "2020-01-01",
            "check_out": "2020-01-05",
        },
        "headers": default_headers,
    }

    context: Dict = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 202
    body = response["body"]
    assert body == "Booking request is in progress"


def test_booking_when_a_day_is_not_available(
    listings_collection_one_room, users_collection, default_headers
):
    """
    Test if function works with one room in the database
    """
    sample_room = listings_collection_one_room.find()[0]
    event = {
        "body": {
            "room": sample_room["_id"],
            "check_in": "2020-01-04",
            "check_out": "2020-01-14",
        },
        "headers": default_headers,
    }

    context: Dict = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 400
    body = response["body"]
    assert body == "Dates are not available"


def test_booking_when_room_id_is_wrong(
    listings_collection_one_room, users_collection, default_headers
):
    """
    Test if function works with one room in the database
    """
    event = {
        "body": {
            "room": 21,
            "check_in": "2020-01-04",
            "check_out": "2020-01-14",
        },
        "headers": default_headers,
    }

    context: Dict = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 404
    body = response["body"]
    assert body == "Room not found"


def test_booking_with_unauthorized_user(listings_collection_one_room):
    """
    Test if function works with one room in the database
    """
    event = {
        "body": {
            "room": 21,
            "check_in": "2020-01-04",
            "check_out": "2020-01-14",
        },
    }

    context: Dict = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 401
    body = response["body"]
    assert body == "Unauthorized"
