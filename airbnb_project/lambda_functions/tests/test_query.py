"""
Test functionality of query lambda functions with following tests
1. Health check and testing with no query parameters
2. Testing with query parameters with area
3. Testing with query parameters with check in and check out
4. Testing with query parameters with check in and check out with no rooms
"""
# pylint: disable=unused-argument

from typing import Dict, List
from models import QueryEvent
from models import Room
from query import lambda_handler


def test_query_base(listings_collection_one_room, sample_room: Room):
    """
    Test if function works with one room in the database
    """
    event: QueryEvent = QueryEvent()
    context: Dict = {}
    response = lambda_handler(event.dict(), context)
    assert response["statusCode"] == 200
    body = response["body"]
    response_room = body[0]
    assert response_room == sample_room.dict()


def test_query_with_area(listings_collection, sample_rooms: List[Room]):
    """Test query with area"""
    room = sample_rooms[0].dict()
    area = room["neighborhood"]
    event: QueryEvent = QueryEvent(
        **{
            "queryStringParameters": {
                "area": area,
            }
        }
    )

    context: Dict = {}
    response = lambda_handler(event.dict(), context)
    expected_rooms = [room.dict() for room in sample_rooms if room.neighborhood == area]
    body = response["body"]

    assert response["statusCode"] == 200
    assert len(body) == len(expected_rooms)
    assert len(body) != len(sample_rooms)


def test_query_with_check_in_check_out(listings_collection, sample_rooms: List[Room]):
    """Test query with check in and check out"""
    room = sample_rooms[0]
    check_in = room.calendar[0].date
    check_out = room.calendar[-1].date
    event: QueryEvent = QueryEvent(
        **{
            "queryStringParameters": {
                "check_in": check_in,
                "check_out": check_out,
            }
        }
    )
    context: Dict = {}
    response = lambda_handler(event.dict(), context)

    # because of the way the database is set up, the query will return all rooms
    expected_rooms = [room.dict() for room in sample_rooms]
    body = response["body"]

    assert response["statusCode"] == 200
    assert len(body) == len(expected_rooms)


def test_query_with_check_in_check_out_empty(listings_collection, sample_rooms):
    """Test query with check in and check out"""
    room = sample_rooms[0].dict()
    check_in = room["calendar"][11]["date"]
    check_out = room["calendar"][18]["date"]
    event: QueryEvent = QueryEvent(
        **{
            "queryStringParameters": {
                "check_in": check_in,
                "check_out": check_out,
            }
        }
    )
    context: Dict = {}
    response = lambda_handler(event.dict(), context)

    body = response["body"]

    assert response["statusCode"] == 200
    assert len(body) == 0
