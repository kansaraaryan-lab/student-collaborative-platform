from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db

from backend.app.schemas.event import (
    EventCreate,
    EventResponse,
    EventUpdate,
)
from backend.app.services.events import (
    create_event,
    delete_event,
    get_event,
    get_events,
    get_event_status,
    update_event,
)

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event_endpoint(
    event_data: EventCreate,
    db: Session = Depends(get_db),
):
    event = create_event(db, event_data)

    return EventResponse(
        **event.__dict__,
        status=get_event_status(event),
    )


@router.get(
    "",
    response_model=list[EventResponse],
)
def list_events(
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    db: Session = Depends(get_db),
):
    if status_filter not in {
        None,
        "ongoing",
        "upcoming",
        "previous",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "status must be one of: "
                "ongoing, upcoming, previous"
            ),
        )

    events = get_events(
        db,
        status_filter,
    )

    return [
        EventResponse(
            **event.__dict__,
            status=get_event_status(event),
        )
        for event in events
    ]


@router.get(
    "/{event_id}",
    response_model=EventResponse,
)
def get_event_endpoint(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = get_event(db, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return EventResponse(
        **event.__dict__,
        status=get_event_status(event),
    )


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
)
def update_event_endpoint(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
):
    event = get_event(db, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    try:
        event = update_event(
            db,
            event,
            event_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return EventResponse(
        **event.__dict__,
        status=get_event_status(event),
    )


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event_endpoint(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = get_event(db, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    delete_event(db, event)