from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    event_type: str
    start_time: datetime
    end_time: datetime
    location: str | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_type: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    location: str | None = None


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None
    event_type: str
    start_time: datetime
    end_time: datetime
    location: str | None
    created_by: int
    created_at: datetime
    updated_at: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)


