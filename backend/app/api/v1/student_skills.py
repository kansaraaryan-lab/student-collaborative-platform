from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.student import Student
from backend.app.models.skill import Skill
from backend.app.models.student_skill import StudentSkill
from backend.app.schemas.student_skill import (
    StudentSkillCreate,
    StudentSkillResponse,
)

router = APIRouter()


@router.post(
    "/student-skills",
    response_model=StudentSkillResponse,
)
async def add_student_skill(
    student_skill: StudentSkillCreate,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_skill.student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    skill = (
        db.query(Skill)
        .filter(Skill.id == student_skill.skill_id)
        .first()
    )

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    existing = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_id == student_skill.student_id,
            StudentSkill.skill_id == student_skill.skill_id,
        )
        .first()
    )

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Student already has this skill",
        )

    new_student_skill = StudentSkill(
        student_id=student_skill.student_id,
        skill_id=student_skill.skill_id,
        proficiency=student_skill.proficiency,
    )
    db.add(new_student_skill)
    db.commit()
    db.refresh(new_student_skill)

    return new_student_skill

@router.get(
    "/students/{student_id}/skills",
    response_model=list[StudentSkillResponse],
)
async def get_student_skills(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    student_skills = (
        db.query(StudentSkill)
        .filter(StudentSkill.student_id == student_id)
        .all()
    )

    return student_skills

@router.delete("/students/{student_id}/skills/{skill_id}")
async def delete_student_skill(
    student_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
):
    student_skill = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_id == student_id,
            StudentSkill.skill_id == skill_id,
        )
        .first()
    )

    if student_skill is None:
        raise HTTPException(
            status_code=404,
            detail="Student skill not found",
        )

    db.delete(student_skill)
    db.commit()

    return {
        "message": "Student skill removed successfully"
    }