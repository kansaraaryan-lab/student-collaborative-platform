from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    college_email: str
    name: str
    room_id: int

class StudentUpdate(BaseModel):
    college_email: str | None = None
    name: str | None = None
    room_id: int | None = None

class StudentResponse(BaseModel):
    id: int
    college_email: str
    name: str
    room_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
