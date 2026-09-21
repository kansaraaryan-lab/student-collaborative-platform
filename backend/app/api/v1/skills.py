from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.skill import Skill
from backend.app.schemas.skill import (
    SkillCreate,
    SkillUpdate,
    SkillResponse,
)

router = APIRouter()


@router.post(
    "/skills",
    response_model=SkillResponse,
)
async def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
):
    existing_skill = (
        db.query(Skill)
        .filter(Skill.name == skill.name)
        .first()
    )

    if existing_skill is not None:
        raise HTTPException(
            status_code=409,
            detail="Skill already exists",
        )

    new_skill = Skill(
        name=skill.name,
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get(
    "/skills",
    response_model=list[SkillResponse],
)
async def get_skills(
    db: Session = Depends(get_db),
):
    skills = db.query(Skill).all()
    return skills


@router.get(
    "/skills/{skill_id}",
    response_model=SkillResponse,
)
async def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
):
    skill = (
        db.query(Skill)
        .filter(Skill.id == skill_id)
        .first()
    )

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    return skill


@router.patch(
    "/skills/{skill_id}",
    response_model=SkillResponse,
)
async def update_skill(
    skill_id: int,
    skill: SkillUpdate,
    db: Session = Depends(get_db),
):
    existing_skill = (
        db.query(Skill)
        .filter(Skill.id == skill_id)
        .first()
    )

    if existing_skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    update_data = skill.model_dump(exclude_unset=True)

    if "name" in update_data:
        duplicate_skill = (
            db.query(Skill)
            .filter(
                Skill.name == update_data["name"],
                Skill.id != skill_id,
            )
            .first()
        )

        if duplicate_skill is not None:
            raise HTTPException(
                status_code=409,
                detail="Skill already exists",
            )

    for field, value in update_data.items():
        setattr(existing_skill, field, value)

    db.commit()
    db.refresh(existing_skill)

    return existing_skill


@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
):
    skill = (
        db.query(Skill)
        .filter(Skill.id == skill_id)
        .first()
    )

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    db.delete(skill)
    db.commit()

    return {
        "message": "Skill deleted successfully"
    }