import httpx
import pytest

from starfall.ingestion.nasa import NasaNeoClient


def test_fetch_feed_returns_json_and_sends_parameters() -> None:
    def mock_handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/neo/rest/v1/feed"
        assert request.url.params["start_date"] == "2030-01-15"
        assert request.url.params["end_date"] == "2030-01-15"
        assert request.url.params["api_key"] == "test_key"

        return httpx.Response(
            200,
            json={"near_earth_objects": {"2030-01-15": []}},
        )

    transport = httpx.MockTransport(mock_handler)

    with httpx.Client(transport=transport) as http_client:
        client = NasaNeoClient(api_key="test_key", client=http_client)
        result = client.fetch_feed("2030-01-15", "2030-01-15")

    assert result == {"near_earth_objects": {"2030-01-15": []}}

def test_fetch_feed_raises_for_http_error() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(500, json={"error": "Internal Server Error"})
    )

    with httpx.Client(transport=transport) as http_client:
        client = NasaNeoClient(api_key="test_key", client=http_client)

        with pytest.raises(httpx.HTTPStatusError):
            client.fetch_feed("2030-01-15", "2030-01-15")