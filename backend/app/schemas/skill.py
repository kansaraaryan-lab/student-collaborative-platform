from pydantic import BaseModel, ConfigDict


class SkillCreate(BaseModel):
    name: str


class SkillUpdate(BaseModel):
    name: str | None = None


class SkillResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)