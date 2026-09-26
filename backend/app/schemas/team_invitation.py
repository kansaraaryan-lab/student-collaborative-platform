from pydantic import BaseModel


class TeamInvitationUpdate(BaseModel):
    status: str

