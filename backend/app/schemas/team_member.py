from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamMemberCreate(BaseModel):
    student_id: int


class TeamMemberResponse(BaseModel):
    id: int
    team_id: int
    student_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)