from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from starfall.domain.models import CloseApproach
from starfall.ingestion.nasa import NasaNeoClient, parse_neo_feed

app = FastAPI(
    title="Starfall API",
    description="Explore near-Earth asteroids and their close approaches.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/")
def root() -> dict[str, str]:
    """Return basic information about the Starfall API."""
    return {
        "name": "Starfall API",
        "message": "Welcome to the Starfall asteroid explorer!",
    }

@app.get("/health")
def health() -> dict[str, str]:
    """Return the health status of the Starfall API."""
    return {"status": "healthy"}    

@app.get("/api/approaches", response_model=list[CloseApproach])
def get_approaaches(
    start_date: date = Query(description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(description="End date (YYYY-MM-DD)"),
) -> list[CloseApproach]:
    """Return aestroid close approaches within the specified date range."""
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be greater than or equal to start date.",
        )

    if (end_date - start_date).days > 7:
        raise HTTPException(
            status_code=400,
            detail="Date range must not exceed 7 days.",
        )

    try:    
        client = NasaNeoClient()
        payload = client.fetch_feed(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )
        return parse_neo_feed(payload)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch or parse NASA data: {str(e)}",
        )
