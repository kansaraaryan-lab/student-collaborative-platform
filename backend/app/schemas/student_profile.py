from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentProfileCreate(BaseModel):
    bio: str | None = None
    profile_picture: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None


class StudentProfileUpdate(BaseModel):
    bio: str | None = None
    profile_picture: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None


class StudentProfileResponse(BaseModel):
    student_id: int
    bio: str | None
    profile_picture: str | None
    github_url: str | None
    linkedin_url: str | None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)