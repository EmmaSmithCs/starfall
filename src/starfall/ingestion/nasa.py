import os
from typing import Any
from dotenv import load_dotenv

import httpx

from starfall.domain.models import CloseApproach

load_dotenv()

def parse_neo_feed(payload: dict[str, Any]) -> list[CloseApproach]:
    """Convert a NASA NeoWs feed response into validated CloseApproach records."""
    near_earth_objects = payload.get("near_earth_objects")

    if not isinstance(near_earth_objects, dict):
        raise ValueError("NASA response is missing near_earth_objects")

    approaches: list[CloseApproach] = []

    for asteroids in near_earth_objects.values():
        if not isinstance(asteroids, list):
            raise ValueError("Expected each date to contain a list of asteroids")

        for asteroid in asteroids:
            for approach in asteroid.get("close_approach_data", []):
                approaches.append(
                    CloseApproach(
                        nasa_id=asteroid["id"],
                        name=asteroid["name"],
                        approach_date=approach["close_approach_date"],
                        miss_distance_km=float(
                            approach["miss_distance"]["kilometers"]
                        ),
                        relative_velocity_kph=float(
                            approach["relative_velocity"]["kilometers_per_hour"]
                        ),
                        is_potentially_hazardous=asteroid[
                            "is_potentially_hazardous_asteroid"
                        ]
                    )
                )
    return approaches

class NasaNeoClient:
    """HTTP client for NASA's Near Earth Object Web Service."""

    BASE_URL = "https://api.nasa.gov/neo/rest/v1"

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = 10.0,
        client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("NASA_API_KEY", "DEMO_KEY")
        self.timeout = timeout
        self._client = client

    def fetch_feed(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Fetch near-Earth objects for an inclusive date range."""
        request_client = self._client or httpx.Client()
        try:
            response = request_client.get(
                f"{self.BASE_URL}/feed",
                params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "api_key": self.api_key,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload: dict[str, Any] = response.json()
            return payload
        finally:
            if self._client is None:
                request_client.close()
