from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    event_type: str
    start_time: datetime
    end_time: datetime
    location: str | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        return self


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_type: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    location: str | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time <= self.start_time
        ):
            raise ValueError("end_time must be greater than start_time")

        return self


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None
    event_type: str
    start_time: datetime
    end_time: datetime
    location: str | None
    created_at: datetime
    status: str

    model_config = ConfigDict(from_attributes=True) 