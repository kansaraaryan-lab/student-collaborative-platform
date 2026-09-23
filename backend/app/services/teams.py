from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.event import Event
from backend.app.models.student import Student
from backend.app.models.team import Team
from backend.app.models.team_member import TeamMember
from backend.app.schemas.team import TeamCreate, TeamUpdate
from backend.app.schemas.team_member import TeamMemberCreate


def get_team(db: Session, team_id: int) -> Team | None:
    return db.scalar(
        select(Team).where(Team.id == team_id)
    )


def get_team_member(
    db: Session,
    team_id: int,
    student_id: int,
) -> TeamMember | None:
    return db.scalar(
        select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.student_id == student_id,
        )
    )


def get_team_members(
    db: Session,
    team_id: int,
) -> list[TeamMember]:
    return list(
        db.scalars(
            select(TeamMember)
            .where(TeamMember.team_id == team_id)
            .order_by(TeamMember.joined_at)
        ).all()
    )


def get_team_member_count(
    db: Session,
    team_id: int,
) -> int:
    return db.scalar(
        select(func.count(TeamMember.id))
        .where(TeamMember.team_id == team_id)
    ) or 0


def get_next_team_number(
    db: Session,
    event_id: int,
) -> int:
    existing_team_numbers = db.scalars(
        select(Team.name)
        .where(
            Team.event_id == event_id,
            Team.name.like("Team-%"),
        )
    ).all()

    numbers = []

    for name in existing_team_numbers:
        try:
            number = int(name.removeprefix("Team-"))
            numbers.append(number)
        except ValueError:
            continue

    return max(numbers, default=0) + 1


def create_team(
    db: Session,
    team_data: TeamCreate,
    student_id: int,
) -> Team:
    event = db.scalar(
        select(Event).where(Event.id == team_data.event_id)
    )

    if event is None:
        raise ValueError("Event not found")

    student = db.scalar(
        select(Student).where(Student.id == student_id)
    )

    if student is None:
        raise ValueError("Student not found")

    existing_event_membership = db.scalar(
        select(TeamMember)
        .join(
            Team,
            Team.id == TeamMember.team_id,
        )
        .where(
            Team.event_id == team_data.event_id,
            TeamMember.student_id == student_id,
            )
    )

    if existing_event_membership is not None:
        raise ValueError(
            "Student is already a member of a team for this event"
        )

    team_number = get_next_team_number(
        db,
        team_data.event_id,
    )

    team = Team(
        name=f"Team-{team_number}",
        description=team_data.description,
        event_id=team_data.event_id,
        created_by=student_id,
        leader_id=student_id,
        max_members=team_data.max_members,
        status="open",
    )

    db.add(team)
    db.flush()

    creator_membership = TeamMember(
        team_id=team.id,
        student_id=student_id,
    )

    db.add(creator_membership)

    db.commit()
    db.refresh(team)

    return team


def update_team(
    db: Session,
    team: Team,
    team_data: TeamUpdate,
) -> Team:
    update_data = team_data.model_dump(exclude_unset=True)

    if "status" in update_data:
        if update_data["status"] not in {
            "open",
            "full",
            "closed",
        }:
            raise ValueError(
                "status must be one of: open, full, closed"
            )

    if "max_members" in update_data:
        current_member_count = get_team_member_count(
            db,
            team.id,
        )

        if update_data["max_members"] < current_member_count:
            raise ValueError(
                "max_members cannot be less than the current member count"
            )

    for field, value in update_data.items():
        setattr(team, field, value)

    db.commit()
    db.refresh(team)

    return team


def add_team_member(
    db: Session,
    team: Team,
    member_data: TeamMemberCreate,
) -> TeamMember:
    student = db.scalar(
        select(Student).where(
            Student.id == member_data.student_id
        )
    )

    if student is None:
        raise ValueError("Student not found")

    existing_membership = get_team_member(
        db,
        team.id,
        member_data.student_id,
    )

    if existing_membership is not None:
        raise ValueError(
            "Student is already a member of this team"
        )

    current_member_count = get_team_member_count(
        db,
        team.id,
    )

    if current_member_count >= team.max_members:
        raise ValueError("Team is full")

    if team.status != "open":
        raise ValueError("Team is not open for new members")

    if team.event_id is not None:
        existing_event_membership = db.scalar(
            select(TeamMember)
            .join(
                Team,
                Team.id == TeamMember.team_id,
            )
            .where(
                Team.event_id == team.event_id,
                TeamMember.student_id
                == member_data.student_id,
            )
        )

        if existing_event_membership is not None:
            raise ValueError(
                "Student is already a member of another team "
                "for this event"
            )

    membership = TeamMember(
        team_id=team.id,
        student_id=member_data.student_id,
    )

    db.add(membership)

    db.flush()

    new_member_count = current_member_count + 1

    if new_member_count >= team.max_members:
        team.status = "full"

    db.commit()
    db.refresh(membership)

    return membership


def remove_team_member(
    db: Session,
    team: Team,
    student_id: int,
) -> None:
    membership = get_team_member(
        db,
        team.id,
        student_id,
    )

    if membership is None:
        raise ValueError(
            "Student is not a member of this team"
        )

    if team.leader_id == student_id:
        raise ValueError(
            "Team leader must transfer leadership before leaving"
        )

    if team.event_id is not None:
        event = db.scalar(
            select(Event).where(
                Event.id == team.event_id
            )
        )

        if event is not None:
            now = datetime.now(timezone.utc)
            leave_deadline = (
                event.start_time
                - timedelta(hours=48)
            )

            if now >= leave_deadline:
                raise ValueError(
                    "Students cannot leave the team "
                    "within 48 hours of the event"
                )

    db.delete(membership)

    if team.status == "full":
        team.status = "open"

    db.commit()


def transfer_leadership(
    db: Session,
    team: Team,
    current_leader_id: int,
    new_leader_id: int,
) -> Team:
    if team.leader_id != current_leader_id:
        raise ValueError(
            "Only the current team leader can transfer leadership"
        )

    if current_leader_id == new_leader_id:
        raise ValueError(
            "New leader must be different from current leader"
        )

    new_leader_membership = get_team_member(
        db,
        team.id,
        new_leader_id,
    )

    if new_leader_membership is None:
        raise ValueError(
            "New leader must already be a team member"
        )

    team.leader_id = new_leader_id

    db.commit()
    db.refresh(team)

    return team


def delete_team(
    db: Session,
    team: Team,
) -> None:
    db.delete(team)
    db.commit()