from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.event import Event
from backend.app.schemas.event import EventCreate, EventUpdate


def get_event_status(event: Event) -> str:
    now = datetime.now(timezone.utc)

    if now < event.start_time:
        return "upcoming"

    if now <= event.end_time:
        return "ongoing"

    return "previous"


def create_event(
    db: Session,
    event_data: EventCreate,
) -> Event:
    event = Event(
        title=event_data.title,
        description=event_data.description,
        event_type=event_data.event_type,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        location=event_data.location,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_events(
    db: Session,
    status: str | None = None,
) -> list[Event]:

    events = db.scalars(
        select(Event).order_by(Event.start_time)
    ).all()

    if status is None:
        return list(events)

    return [
        event
        for event in events
        if get_event_status(event) == status
    ]


def get_event(
    db: Session,
    event_id: int,
) -> Event | None:

    return db.scalar(
        select(Event).where(Event.id == event_id)
    )


def update_event(
    db: Session,
    event: Event,
    event_data: EventUpdate,
) -> Event:

    update_data = event_data.model_dump(
        exclude_unset=True
    )

    new_start_time = update_data.get(
        "start_time",
        event.start_time,
    )

    new_end_time = update_data.get(
        "end_time",
        event.end_time,
    )

    if new_end_time <= new_start_time:
        raise ValueError(
            "end_time must be greater than start_time"
        )

    for field, value in update_data.items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)

    return event


def delete_event(
    db: Session,
    event: Event,
) -> None:

    db.delete(event)
    db.commit()