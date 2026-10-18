from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CloseApproach(BaseModel):
    """A validated close_approach record for a near-Earth object."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    nasa_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    approach_date: date
    miss_distance_km: float = Field(ge=0, allow_inf_nan=False)
    relative_velocity_kph: float = Field(gt=0, allow_inf_nan=False)
    is_potentially_hazardous: bool