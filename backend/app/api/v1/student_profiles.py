from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.student import Student
from backend.app.models.student_profile import StudentProfile
from backend.app.schemas.student_profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
)

router = APIRouter()


@router.post(
    "/students/{student_id}/profile",
    response_model=StudentProfileResponse,
)
async def create_student_profile(
    student_id: int,
    profile: StudentProfileCreate,
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

    existing_profile = (
        db.query(StudentProfile)
        .filter(StudentProfile.student_id == student_id)
        .first()
    )

    if existing_profile is not None:
        raise HTTPException(
            status_code=409,
            detail="Student profile already exists",
        )

    new_profile = StudentProfile(
        student_id=student_id,
        bio=profile.bio,
        profile_picture=profile.profile_picture,
        github_url=profile.github_url,
        linkedin_url=profile.linkedin_url,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get(
    "/students/{student_id}/profile",
    response_model=StudentProfileResponse,
)
async def get_student_profile(
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

    profile = (
        db.query(StudentProfile)
        .filter(StudentProfile.student_id == student_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    return profile

@router.patch(
    "/students/{student_id}/profile",
    response_model=StudentProfileResponse,
)
async def update_student_profile(
    student_id: int,
    profile: StudentProfileUpdate,
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

    existing_profile = (
        db.query(StudentProfile)
        .filter(StudentProfile.student_id == student_id)
        .first()
    )

    if existing_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    update_data = profile.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_profile, field, value)

    db.commit()
    db.refresh(existing_profile)

    return existing_profile