from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TeamCreate(BaseModel):
    description: str | None = None
    event_id: int
    max_members: int = Field(default=4, ge=2, le=20)


class TeamUpdate(BaseModel):
    description: str | None = None
    max_members: int | None = Field(
        default=None,
        ge=2,
        le=20,
    )
    status: str | None = None


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str | None
    event_id: int | None
    created_by: int
    leader_id: int
    max_members: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)