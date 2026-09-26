from fastapi import APIRouter, Depends, HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.student import Student


router = APIRouter(prefix="/auth", tags=["Authentication"])


class GoogleLoginRequest(BaseModel):
    credential: str


@router.post("/google")
async def google_login(
    data: GoogleLoginRequest,
    db: Session = Depends(get_db),
):
    try:
        google_user = id_token.verify_oauth2_token(
            data.credential,
            requests.Request(),
            settings.google_client_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google credential",
        )

    email = google_user.get("email")
    email_verified = google_user.get("email_verified", False)

    if not email or not email_verified:
        raise HTTPException(
            status_code=401,
            detail="Google email is not verified",
        )

    email = email.lower()

    if not email.endswith("@sjcem.edu.in"):
        raise HTTPException(
            status_code=403,
            detail="Only @sjcem.edu.in accounts are allowed",
        )

    student = (
        db.query(Student)
        .filter(Student.college_email == email)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=403,
            detail="College account is not registered",
        )

    return {
        "message": "Login successful",
        "student": {
            "id": student.id,
            "college_email": student.college_email,
            "name": student.name,
            "room_id": student.room_id,
        },
    }