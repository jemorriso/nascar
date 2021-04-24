import pytest
import json
import os

from dotenv import load_dotenv

from src.nascar.nascar import Drivers

load_dotenv()


@pytest.fixture
def nascar_data():
    with open(f"{os.getenv('PROJECT_ROOT')}/src/nascar/data/lap-times.json", "r") as f:
        return json.load(f)


@pytest.fixture
def drivers(nascar_data):
    drivers = Drivers(nascar_data["laps"])
    return drivers


def test_init_drivers(nascar_data):
    drivers = Drivers(nascar_data["laps"])
    for v in drivers.drivers.values():
        assert v.id is not None
        assert v.manufacturer is not None
        assert v.number is not None
        assert v.name is not None


def test_update_lap_times(nascar_data, drivers):
    drivers.update_lap_times(nascar_data["laps"])
