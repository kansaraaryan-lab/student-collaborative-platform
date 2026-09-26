from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.message import Message
from backend.app.models.student import Student
from backend.app.schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get(
    "/{student_id}",
    response_model=list[MessageResponse],
)
async def get_messages(
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

    messages = (
        db.query(Message)
        .filter(
            or_(
                Message.sender_id == student_id,
                Message.receiver_id == student_id,
            )
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    return messages


@router.post(
    "",
    response_model=MessageResponse,
)
async def create_message(
    data: MessageCreate,
    student_id: int,
    db: Session = Depends(get_db),
):
    receiver = (
        db.query(Student)
        .filter(Student.id == data.receiver_id)
        .first()
    )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found",
        )

    message = Message(
        sender_id=student_id,
        receiver_id=data.receiver_id,
        content=data.content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

