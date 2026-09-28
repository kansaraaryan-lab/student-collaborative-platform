from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.websocket import manager
from backend.app.models.message import Message
from backend.app.models.student import Student


router = APIRouter(
    prefix="/ws",
    tags=["Messages WebSocket"],
)


@router.websocket("/messages/{student_id}")
async def message_websocket(
    websocket: WebSocket,
    student_id: int,
    db: Session = Depends(get_db),
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        await websocket.close(code=1008)
        return

    await manager.connect(student_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            receiver_id = data.get("receiver_id")
            content = data.get("content")

            if not receiver_id or not content:
                continue

            receiver = (
                db.query(Student)
                .filter(Student.id == receiver_id)
                .first()
            )

            if receiver is None:
                continue

            message = Message(
                sender_id=student_id,
                receiver_id=receiver_id,
                content=content,
            )

            db.add(message)
            db.commit()
            db.refresh(message)

            message_data = {
                "id": message.id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }

            await manager.send_to_student(
                receiver_id,
                message_data,
            )

            await manager.send_to_student(
                student_id,
                message_data,
            )

    except WebSocketDisconnect:
        manager.disconnect(student_id)

