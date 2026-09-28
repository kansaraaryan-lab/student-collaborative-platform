from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.student import Student
from backend.app.schemas.student import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter()

@router.post("/students", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
):
    new_student = Student(
        college_email=student.college_email,
        name=student.name,
        room_id=student.room_id,
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/students", response_model=list[StudentResponse])
async def get_students(
    db: Session = Depends(get_db),
):
    students = db.query(Student).all()

    return students

@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(
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

    return student

@router.patch("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
):
    existing_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    update_data = student.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_student, field, value)

    db.commit()
    db.refresh(existing_student)

    return existing_student

@router.delete("/students/{student_id}")
async def delete_student(
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

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
    }