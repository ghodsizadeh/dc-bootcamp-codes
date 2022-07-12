"""
Pytest fixtures
"""
# pylint: disable=unused-argument

import pymongo
import pytest
from faker import Faker

fake = Faker()
Faker.seed(0)


def host_faker():
    """
    A utility function to generate a host object
    """
    return {
        "host_id": fake.random_int(min=1000, max=10000),
        "host_name": fake.name(),
    }


def calendar_faker():
    """
    A utility function to generate a calendar object
    """
    price = fake.random_int(min=100, max=1000)
    return [
        {
            "date": f"2020-01-{i:02d}",
            "price": price,
            "adjusted_price": price,
            "availability": not 10 < i < 20,
        }
        for i in range(30)
    ]


def room_generator():
    """
    A utility function to generate a room object
    """
    return {
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


@pytest.fixture(name="sample_room")
def fixture_sample_room():
    """
    A fixture to generate a room object
    """
    return room_generator()


@pytest.fixture
def listings_collection_one_room(sample_room):
    """
    A fixture to generate a collection of one room
    then clean it up after the test
    """
    client = pymongo.MongoClient()
    db = client.airbnb
    collection = db.listings
    collection.insert_one(sample_room)
    yield collection
    collection.delete_many({})


@pytest.fixture(name="sample_rooms")
def fixture_sample_rooms():
    """
    A fixture to generate a collection of rooms
    """
    return [room_generator() for _ in range(20)]


@pytest.fixture
def listings_collection(sample_rooms):
    """
    A fixture to generate a collection of rooms
    then clean it up after the test
    """

    client = pymongo.MongoClient()
    db = client.airbnb
    collection = db.listings
    collection.insert_many(sample_rooms)
    yield collection
    collection.delete_many({})
