from pydantic import BaseModel, ConfigDict


class StudentSkillCreate(BaseModel):
    student_id: int
    skill_id: int
    proficiency: str


class StudentSkillResponse(BaseModel):
    student_id: int
    skill_id: int
    proficiency: str

    model_config = ConfigDict(from_attributes=True)