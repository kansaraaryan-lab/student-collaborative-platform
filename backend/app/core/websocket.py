from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(
        self,
        student_id: int,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.active_connections[student_id] = websocket

    def disconnect(self, student_id: int):
        self.active_connections.pop(student_id, None)

    async def send_to_student(
        self,
        student_id: int,
        message: dict,
    ):
        websocket = self.active_connections.get(student_id)

        if websocket:
            await websocket.send_json(message)


manager = ConnectionManager()

