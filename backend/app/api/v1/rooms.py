from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.room import Room
from backend.app.schemas.room import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter()


@router.post("/rooms", response_model=RoomResponse)
async def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
):
    new_room = Room(
        year=room.year,
        branch=room.branch,
        division=room.division,
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room

@router.get("/rooms", response_model=list[RoomResponse])
async def get_rooms(
    db: Session = Depends(get_db),
):
    rooms = db.query(Room).all()

    return rooms

@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )
    return room

@router.patch("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
):
    existing_room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if existing_room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    update_data = room.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_room, field, value)

    db.commit()
    db.refresh(existing_room)

    return existing_room

@router.delete("/rooms/{room_id}")
async def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    db.delete(room)
    db.commit()

    return {
        "message": "Room deleted successfully",
    }