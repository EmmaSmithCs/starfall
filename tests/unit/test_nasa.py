import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from starfall.domain.models import CloseApproach
from starfall.ingestion.nasa import parse_neo_feed

FIXTURE_PATH = Path(__file__).parents[1] / "fixtures" / "nasa_neo_feed.json"

def test_parse_neo_feed_returns_validated_approach() -> None:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    approaches = parse_neo_feed(payload)

    assert len(approaches) == 1
    assert isinstance(approaches[0], CloseApproach)
    assert approaches[0].nasa_id == "54321"
    assert approaches[0].name == "Example Asteroid"
    assert approaches[0].miss_distance_km == 750_000.0
    assert approaches[0].relative_velocity_kph == 42_000.0
    assert approaches[0].is_potentially_hazardous is False

def test_parse_neo_feed_rejects_invalid_model_data() -> None:
    payload = {
        "near_earth_objects": {
            "2023-01-15": [
                {
                    "id": "",
                    "name": "Example Asteroid",
                    "is_potentially_hazardous_asteroid": False,
                    "close_approach_data": [
                        {
                            "close_approach_date": "2030-01-15",
                            "relative_velocity": {
                                "kilometers_per_hour": "42000.0"
                            },
                            "miss_distance": {"kilometers": "750000.0"}
                        }
                    ]
                }
            ],
        }
    }

    with pytest.raises(ValidationError):
        parse_neo_feed(payload)