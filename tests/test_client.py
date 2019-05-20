"""Test the backend client."""

from configparser import ConfigParser
from random import choices
from string import ascii_lowercase

from pytest import fixture, raises

from plateypus import client

BACKEND = "http://backend.invalid"


def random_str(length=16):
    """Return a random string of the given length."""
    return "".join(choices(ascii_lowercase, k=length))


@fixture
def plateypus_client():
    """Yield a backend client fixture."""
    config = ConfigParser()
    config["BACKEND"] = {"url": BACKEND}
    yield client.PlateypusClient(config)


def test_search(plateypus_client, requests_mock):
    """Test that search works."""
    _id = random_str()
    requests_mock.post(
        f"{BACKEND}/search", json=[dict(_id=_id, _type="_doc")], status_code=200
    )
    search = plateypus_client.search(dict(plate=random_str()))
    assert search[0]["_id"] == _id


def test_bad_search(plateypus_client, requests_mock):
    """Test that searching with malformed payload returns 400."""
    requests_mock.post(
        f"{BACKEND}/search", json=dict(fields=["required field"]), status_code=400
    )
    with raises(RuntimeError) as rerr:
        plateypus_client.search(dict(foo=42))
    assert rerr.match("Unexpected result: 400")


def test_vehicle(plateypus_client, requests_mock):
    """Test that a vehicle is returned if you know the id."""
    _id = random_str()
    requests_mock.get(f"{BACKEND}/vehicle/{_id}", json=dict(plate="foo"))
    vehicle = plateypus_client.vehicle(_id)
    assert vehicle["plate"] == "foo"


def test_vehicle_not_found(plateypus_client, requests_mock):
    """Test that searching for a non-existing vehicle returns None."""
    _id = random_str()
    requests_mock.get(
        f"{BACKEND}/vehicle/{_id}", json=f"{_id} not found", status_code=404
    )
    assert plateypus_client.vehicle(_id) is None


def test_vehicle_unexpected_error(plateypus_client, requests_mock):
    """Test that unexpected server errors are rethrown."""
    _id = random_str()
    requests_mock.get(
        f"{BACKEND}/vehicle/{_id}", text="internal server error", status_code=500
    )
    with raises(RuntimeError) as rerr:
        plateypus_client.vehicle(_id)
    assert rerr.match("Unexpected server status: 500")
