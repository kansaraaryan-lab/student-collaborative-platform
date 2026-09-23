from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from backend.app.schemas.team_member import (
    TeamMemberCreate,
    TeamMemberResponse,
)
from backend.app.services.teams import (
    add_team_member,
    create_team,
    delete_team,
    get_team,
    get_team_member_count,
    get_team_members,
    remove_team_member,
    transfer_leadership,
    update_team,
)

router = APIRouter(
    prefix="/teams",
    tags=["Teams"],
)


@router.post(
    "",
    response_model=TeamResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_team_endpoint(
    team_data: TeamCreate,
    created_by: int = Query(...),
    db: Session = Depends(get_db),
):
    try:
        team = create_team(
            db,
            team_data,
            created_by,
        )
    except ValueError as exc:
        message = str(exc)

        if "not found" in message:
            code = 404
        else:
            code = 409

        raise HTTPException(
            status_code=code,
            detail=message,
        )

    return team


@router.get(
    "",
    response_model=list[TeamResponse],
)
def list_teams(
    event_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    from sqlalchemy import select
    from backend.app.models.team import Team

    query = select(Team).order_by(Team.id)

    if event_id is not None:
        query = query.where(Team.event_id == event_id)

    return list(db.scalars(query).all())


@router.get(
    "/{team_id}",
    response_model=TeamResponse,
)
def get_team_endpoint(
    team_id: int,
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    return team


@router.patch(
    "/{team_id}",
    response_model=TeamResponse,
)
def update_team_endpoint(
    team_id: int,
    team_data: TeamUpdate,
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    try:
        return update_team(
            db,
            team,
            team_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_team_endpoint(
    team_id: int,
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    delete_team(db, team)


@router.post(
    "/{team_id}/members",
    response_model=TeamMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member_endpoint(
    team_id: int,
    member_data: TeamMemberCreate,
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    try:
        return add_team_member(
            db,
            team,
            member_data,
        )
    except ValueError as exc:
        message = str(exc)

        if "not found" in message:
            code = 404
        else:
            code = 409

        raise HTTPException(
            status_code=code,
            detail=message,
        )


@router.get(
    "/{team_id}/members",
    response_model=list[TeamMemberResponse],
)
def list_members_endpoint(
    team_id: int,
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    return get_team_members(db, team_id)


@router.delete(
    "/{team_id}/members/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member_endpoint(
    team_id: int,
    student_id: int,
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    try:
        remove_team_member(
            db,
            team,
            student_id,
        )
    except ValueError as exc:
        message = str(exc)

        if "not a member" in message:
            code = 404
        else:
            code = 400

        raise HTTPException(
            status_code=code,
            detail=message,
        )


@router.post(
    "/{team_id}/transfer-leadership",
    response_model=TeamResponse,
)
def transfer_leadership_endpoint(
    team_id: int,
    current_leader_id: int = Query(...),
    new_leader_id: int = Query(...),
    db: Session = Depends(get_db),
):
    team = get_team(db, team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    try:
        return transfer_leadership(
            db,
            team,
            current_leader_id,
            new_leader_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )