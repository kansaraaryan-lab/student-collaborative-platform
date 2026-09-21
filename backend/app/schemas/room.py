from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoomCreate(BaseModel):
    year: int
    branch: str | None = None
    division: str


class RoomUpdate(BaseModel):
    year: int | None = None
    branch: str | None = None
    division: str | None = None


class RoomResponse(BaseModel):
    id: int
    year: int
    branch: str | None
    division: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)