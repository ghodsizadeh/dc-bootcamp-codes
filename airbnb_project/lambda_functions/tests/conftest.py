"""
Pytest fixtures
"""
# pylint: disable=unused-argument

from typing import Iterable, List

import pymongo
import pytest
from faker import Faker
from models import Calendar, Host, Room, User

fake = Faker()
Faker.seed(0)


def host_faker() -> Host:
    """
    A utility function to generate a host object
    """
    return Host(
        **{
            "host_id": fake.random_int(min=1000, max=10000),
            "host_name": fake.name(),
        }
    )


def calendar_faker() -> List[Calendar]:
    """
    A utility function to generate a calendar object
    """
    price = fake.random_int(min=100, max=1000)
    return [
        Calendar(
            **{
                "date": f"2020-01-{i:02d}",
                "price": price,
                "adjusted_price": price,
                "availability": not 10 < i < 20,
            }
        )
        for i in range(30)
    ]


def room_generator() -> Room:
    """
    A utility function to generate a room object
    """
    return Room(
        **{
            "name": fake.name(),
            "neighborhood": fake.city(),
            "latitude": float(fake.coordinate(center=0, radius=0.01)),
            "longitude": float(fake.coordinate(center=0, radius=0.01)),
            "room_type": fake.random_element(
                elements=("Entire home", "Private room", "Shared room")
            ),
            "minimum_nights": fake.random_int(min=1, max=10),
            "number_of_reviews": fake.random_int(min=1, max=100),
            "last_review": fake.date(),
            "reviews_per_month": fake.random_int(min=1, max=5),
            "calculated_host_listings_count": fake.random_int(min=1, max=3),
            "number_of_reviews_ltm": 1,
            "availability_365": fake.random_int(min=1, max=365),
            "license": fake.ean(),
            "host": host_faker(),
            "calendar": calendar_faker(),
        }
    )


@pytest.fixture(name="sample_room")
def fixture_sample_room() -> Room:
    """
    A fixture to generate a room object
    """
    return room_generator()


@pytest.fixture
def listings_collection_one_room(
    sample_room: Room,
) -> Iterable[pymongo.collection.Collection]:
    """
    A fixture to generate a collection of one room
    then clean it up after the test
    """
    client: pymongo.MongoClient = pymongo.MongoClient()
    db = client.airbnb
    collection = db.listings
    collection.insert_one(sample_room.dict())
    yield collection
    collection.delete_many({})


@pytest.fixture(name="sample_rooms")
def fixture_sample_rooms() -> List[Room]:
    """
    A fixture to generate a collection of rooms
    """
    return [room_generator() for _ in range(20)]


@pytest.fixture
def listings_collection(
    sample_rooms: List[Room],
) -> Iterable[pymongo.collection.Collection]:
    """
    A fixture to generate a collection of rooms
    then clean it up after the test
    """

    client: pymongo.MongoClient = pymongo.MongoClient()
    db = client.airbnb
    collection = db.listings
    collection.insert_many([room.dict() for room in sample_rooms])
    yield collection
    collection.delete_many({})


@pytest.fixture(name="sample_user")
def fixture_sample_user() -> User:
    """
    A fixture to generate a user object
    """
    return User(
        **{
            "bearer_token": fake.password(),
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
        }
    )


@pytest.fixture
def users_collection(sample_user: User) -> Iterable[pymongo.collection.Collection]:
    """
    A fixture to generate a collection of users
    then clean it up after the test
    """
    client: pymongo.MongoClient = pymongo.MongoClient()
    db = client.airbnb
    collection = db.users
    collection.insert_one(sample_user.dict())
    yield collection
    collection.delete_many({})


@pytest.fixture(name="default_headers")
def fixture_default_header(sample_user: User) -> dict:
    """
    A fixture to generate a default header
    """
    return {
        "Authorization": f"Bearer {sample_user.bearer_token}",
        "Content-Type": "application/json",
    }
