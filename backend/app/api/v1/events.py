from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.event import Event
from backend.app.models.student import Student
from backend.app.schemas.event import (
    EventCreate,
    EventResponse,
    EventUpdate,
)


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("", response_model=list[EventResponse])
async def get_events(
    db: Session = Depends(get_db),
):
    events = (
        db.query(Event)
        .order_by(Event.start_time.asc())
        .all()
    )

    now = datetime.now(timezone.utc)

    response = []

    for event in events:
        if now < event.start_time:
            status = "upcoming"
        elif now < event.end_time:
            status = "ongoing"
        else:
            status = "previous"

        response.append(
            EventResponse(
                id=event.id,
                title=event.title,
                description=event.description,
                event_type=event.event_type,
                start_time=event.start_time,
                end_time=event.end_time,
                location=event.location,
                created_by=event.created_by,
                created_at=event.created_at,
                updated_at=event.updated_at,
                status=status,
            )
        )

    return response


@router.post("", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    x_user_id: int | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="X-User-ID header is required",
        )

    student = (
        db.query(Student)
        .filter(Student.id == x_user_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Student not found",
        )

    if not student.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    new_event = Event(
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        created_by=student.id,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    now = datetime.now(timezone.utc)

    if now < new_event.start_time:
        status = "upcoming"
    elif now < new_event.end_time:
        status = "ongoing"
    else:
        status = "previous"

    return EventResponse(
        id=new_event.id,
        title=new_event.title,
        description=new_event.description,
        event_type=new_event.event_type,
        start_time=new_event.start_time,
        end_time=new_event.end_time,
        location=new_event.location,
        created_by=new_event.created_by,
        created_at=new_event.created_at,
        updated_at=new_event.updated_at,
        status=status,
    )


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event: EventUpdate,
    x_user_id: int | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="X-User-ID header is required",
        )

    student = (
        db.query(Student)
        .filter(Student.id == x_user_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Student not found",
        )

    if not student.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    existing_event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if existing_event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    update_data = event.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_event, field, value)

    db.commit()
    db.refresh(existing_event)

    now = datetime.now(timezone.utc)

    if now < existing_event.start_time:
        status = "upcoming"
    elif now < existing_event.end_time:
        status = "ongoing"
    else:
        status = "previous"

    return EventResponse(
        id=existing_event.id,
        title=existing_event.title,
        description=existing_event.description,
        event_type=existing_event.event_type,
        start_time=existing_event.start_time,
        end_time=existing_event.end_time,
        location=existing_event.location,
        created_by=existing_event.created_by,
        created_at=existing_event.created_at,
        updated_at=existing_event.updated_at,
        status=status,
    )


@router.delete("/{event_id}")
async def delete_event(
    event_id: int,
    x_user_id: int | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="X-User-ID header is required",
        )

    student = (
        db.query(Student)
        .filter(Student.id == x_user_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Student not found",
        )

    if not student.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    existing_event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if existing_event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    db.delete(existing_event)
    db.commit()

    return {
        "message": "Event deleted successfully",
    }