from datetime import date

import pytest
from pydantic import ValidationError

from starfall.domain.models import CloseApproach


def test_valid_close_approach() -> None:
    approach = CloseApproach(
        nasa_id="54321",
        name="Example Asteroid",
        approach_date="2030-01-15",
        miss_distance_km=750_000.0,
        relative_velocity_kph=42_000.0,
        is_potentially_hazardous=False,
    )

    assert approach.nasa_id == "54321"
    assert approach.name == "Example Asteroid"
    assert approach.approach_date == date(2030, 1, 15)
    assert approach.miss_distance_km == 750_000.0
    assert approach.relative_velocity_kph == 42_000.0
    assert approach.is_potentially_hazardous is False

def test_negative_miss_distance_is_rejected() -> None:
    with pytest.raises(ValidationError):
        CloseApproach(
            nasa_id="54321",
            name="Example Asteroid",
            approach_date="2030-01-15",
            miss_distance_km=-1,
            relative_velocity_kph=42_000.0,
            is_potentially_hazardous=False,
        )

def test_zero_relative_velocity_is_rejected() -> None:
    with pytest.raises(ValidationError):
        CloseApproach(
            nasa_id="54321",
            name="Example Asteroid",
            approach_date="2030-01-15",
            miss_distance_km=750_000.0,
            relative_velocity_kph=0,
            is_potentially_hazardous=False,
        )

def test_empty_nasa_if_is_rejected() -> None:
    with pytest.raises(ValidationError):
        CloseApproach(
            nasa_id="",
            name="Example Asteroid",
            approach_date="2030-01-15",
            miss_distance_km=750_000.0,
            relative_velocity_kph=42_000.0,
            is_potentially_hazardous=False,
        )