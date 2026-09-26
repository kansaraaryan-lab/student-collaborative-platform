
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.student import Student
from backend.app.models.skill import Skill
from backend.app.models.student_skill import StudentSkill
from backend.app.models.team_invitation import TeamInvitation
from backend.app.models.team import Team
from backend.app.models.team_member import TeamMember
from backend.app.schemas.team_invitation import TeamInvitationUpdate


router = APIRouter(
    prefix="/team-builder",
    tags=["Team Builder"],
)


@router.get("/candidates")
async def get_candidates(
    db: Session = Depends(get_db),
):
    students = db.query(Student).all()
    candidates = []

    for student in students:
        student_skills = (
            db.query(StudentSkill, Skill)
            .join(
                Skill,
                Skill.id == StudentSkill.skill_id,
            )
            .filter(
                StudentSkill.student_id == student.id
            )
            .all()
        )

        skills = [
            {
                "name": skill.name,
                "proficiency": student_skill.proficiency,
            }
            for student_skill, skill in student_skills
        ]

        candidates.append(
            {
                "student_id": student.id,
                "name": student.name,
                "college_email": student.college_email,
                "skills": skills,
            }
        )

    return candidates


@router.post("/invitations")
async def send_invitation(
    sender_id: int,
    receiver_id: int,
    db: Session = Depends(get_db),
):
    if sender_id == receiver_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot send a request to yourself",
        )

    sender = (
        db.query(Student)
        .filter(Student.id == sender_id)
        .first()
    )

    receiver = (
        db.query(Student)
        .filter(Student.id == receiver_id)
        .first()
    )

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender student not found",
        )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver student not found",
        )

    existing = (
        db.query(TeamInvitation)
        .filter(
            TeamInvitation.sender_id == sender_id,
            TeamInvitation.receiver_id == receiver_id,
            TeamInvitation.status == "pending",
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Invitation already pending",
        )

    invitation = TeamInvitation(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status="pending",
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return {
        "message": "Team invitation sent",
        "invitation_id": invitation.id,
        "sender_id": invitation.sender_id,
        "receiver_id": invitation.receiver_id,
        "status": invitation.status,
    }


@router.get("/invitations/received")
async def get_received_invitations(
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

    invitations = (
        db.query(TeamInvitation)
        .filter(
            TeamInvitation.receiver_id == student_id,
            TeamInvitation.status == "pending",
        )
        .all()
    )

    result = []

    for invitation in invitations:
        sender = (
            db.query(Student)
            .filter(Student.id == invitation.sender_id)
            .first()
        )

        result.append(
            {
                "invitation_id": invitation.id,
                "sender_id": invitation.sender_id,
                "sender_name": (
                    sender.name
                    if sender
                    else "Unknown"
                ),
                "sender_email": (
                    sender.college_email
                    if sender
                    else None
                ),
                "status": invitation.status,
                "created_at": invitation.created_at,
            }
        )

    return result


@router.patch("/invitations/{invitation_id}")
async def update_invitation(
    invitation_id: int,
    invitation_data: TeamInvitationUpdate,
    db: Session = Depends(get_db),
):
    invitation = (
        db.query(TeamInvitation)
        .filter(TeamInvitation.id == invitation_id)
        .first()
    )

    if invitation is None:
        raise HTTPException(
            status_code=404,
            detail="Invitation not found",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Invitation has already been processed",
        )

    if invitation_data.status not in [
        "accepted",
        "rejected",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Status must be accepted or rejected",
        )

    # Reject invitation
    if invitation_data.status == "rejected":
        invitation.status = "rejected"

        db.commit()
        db.refresh(invitation)

        return {
            "message": "Invitation rejected",
            "invitation_id": invitation.id,
            "sender_id": invitation.sender_id,
            "receiver_id": invitation.receiver_id,
            "status": invitation.status,
        }

    # Accept invitation
    sender_id = invitation.sender_id
    receiver_id = invitation.receiver_id

    sender = (
        db.query(Student)
        .filter(Student.id == sender_id)
        .first()
    )

    receiver = (
        db.query(Student)
        .filter(Student.id == receiver_id)
        .first()
    )

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender student not found",
        )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver student not found",
        )

    # Check sender's existing team
    sender_membership = (
        db.query(TeamMember)
        .filter(
            TeamMember.student_id == sender_id
        )
        .first()
    )

    # Check receiver's existing team
    receiver_membership = (
        db.query(TeamMember)
        .filter(
            TeamMember.student_id == receiver_id
        )
        .first()
    )

    # Receiver cannot join another team
    if receiver_membership:
        raise HTTPException(
            status_code=409,
            detail="You are already a member of a team.",
        )

    # Sender already has a team
    if sender_membership:
        team_id = sender_membership.team_id

    # Sender does not have a team
    else:
        team = Team(
            name=f"{sender.name}'s Team",
            created_by=sender_id,
            created_at=datetime.now(timezone.utc),
        )

        db.add(team)
        db.flush()

        team_id = team.id

        # Add sender to new team
        sender_member = TeamMember(
            team_id=team_id,
            student_id=sender_id,
            joined_at=datetime.now(timezone.utc),
        )

        db.add(sender_member)

    # Add receiver to team
    receiver_member = TeamMember(
        team_id=team_id,
        student_id=receiver_id,
        joined_at=datetime.now(timezone.utc),
    )

    db.add(receiver_member)

    # Mark invitation as accepted
    invitation.status = "accepted"

    db.commit()
    db.refresh(invitation)

    return {
        "message": "Invitation accepted and team updated",
        "invitation_id": invitation.id,
        "team_id": team_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "status": invitation.status,
    }


@router.get("/invitations/sent")
async def get_sent_invitations(
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

    invitations = (
        db.query(TeamInvitation)
        .filter(
            TeamInvitation.sender_id == student_id,
            TeamInvitation.status == "pending",
        )
        .all()
    )

    result = []

    for invitation in invitations:
        receiver = (
            db.query(Student)
            .filter(Student.id == invitation.receiver_id)
            .first()
        )

        result.append(
            {
                "invitation_id": invitation.id,
                "receiver_id": invitation.receiver_id,
                "receiver_name": (
                    receiver.name
                    if receiver
                    else "Unknown"
                ),
                "receiver_email": (
                    receiver.college_email
                    if receiver
                    else None
                ),
                "status": invitation.status,
                "created_at": invitation.created_at,
            }
        )

    return result


@router.get("/my-team")
async def get_my_team(
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

    membership = (
        db.query(TeamMember)
        .filter(
            TeamMember.student_id == student_id
        )
        .first()
    )

    if membership is None:
        return {
            "team": None,
            "members": [],
        }

    team = (
        db.query(Team)
        .filter(
            Team.id == membership.team_id
        )
        .first()
    )

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    members = (
        db.query(TeamMember, Student)
        .join(
            Student,
            Student.id == TeamMember.student_id,
        )
        .filter(
            TeamMember.team_id == membership.team_id
        )
        .all()
    )

    return {
        "team": {
            "id": team.id,
            "name": team.name,
            "created_by": team.created_by,
            "created_at": team.created_at,
        },
        "members": [
            {
                "student_id": member_student.id,
                "name": member_student.name,
                "college_email": member_student.college_email,
                "joined_at": member.joined_at,
            }
            for member, member_student in members
        ],
    }


