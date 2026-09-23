import requests


BASE_URL = "http://127.0.0.1:8000/api/v1"


# =========================================================
# STUDENTS
# =========================================================

def get_students():
    response = requests.get(
        f"{BASE_URL}/students",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def create_student(college_email, name, room_id):
    response = requests.post(
        f"{BASE_URL}/students",
        json={
            "college_email": college_email,
            "name": name,
            "room_id": room_id
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


# =========================================================
# ROOMS
# =========================================================

def get_rooms():
    response = requests.get(
        f"{BASE_URL}/rooms",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def create_room(year, branch, division):
    response = requests.post(
        f"{BASE_URL}/rooms",
        json={
            "year": year,
            "branch": branch,
            "division": division
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def update_room(room_id, year, branch, division):
    response = requests.patch(
        f"{BASE_URL}/rooms/{room_id}",
        json={
            "year": year,
            "branch": branch,
            "division": division
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def delete_room(room_id):
    response = requests.delete(
        f"{BASE_URL}/rooms/{room_id}",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


# =========================================================
# SKILLS
# =========================================================

def get_skills():
    response = requests.get(
        f"{BASE_URL}/skills",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def create_skill(name):
    response = requests.post(
        f"{BASE_URL}/skills",
        json={
            "name": name
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def update_skill(skill_id, name):
    response = requests.patch(
        f"{BASE_URL}/skills/{skill_id}",
        json={
            "name": name
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def delete_skill(skill_id):
    response = requests.delete(
        f"{BASE_URL}/skills/{skill_id}",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


# =========================================================
# STUDENT SKILLS
# =========================================================

def add_student_skill(student_id, skill_id, proficiency):
    response = requests.post(
        f"{BASE_URL}/student-skills",
        json={
            "student_id": student_id,
            "skill_id": skill_id,
            "proficiency": proficiency
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def get_student_skills(student_id):
    response = requests.get(
        f"{BASE_URL}/students/{student_id}/skills",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def delete_student_skill(student_id, skill_id):
    response = requests.delete(
        f"{BASE_URL}/students/{student_id}/skills/{skill_id}",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


# =========================================================
# EVENTS
# =========================================================

def get_events(status=None):
    params = {}

    if status:
        params["status"] = status

    response = requests.get(
        f"{BASE_URL}/events",
        params=params,
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def get_event(event_id):
    response = requests.get(
        f"{BASE_URL}/events/{event_id}",
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def create_event(
    title,
    description,
    event_type,
    start_time,
    end_time,
    location
):
    response = requests.post(
        f"{BASE_URL}/events",
        json={
            "title": title,
            "description": description,
            "event_type": event_type,
            "start_time": start_time,
            "end_time": end_time,
            "location": location
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def update_event(
    event_id,
    title=None,
    description=None,
    event_type=None,
    start_time=None,
    end_time=None,
    location=None
):
    data = {}

    if title is not None:
        data["title"] = title

    if description is not None:
        data["description"] = description

    if event_type is not None:
        data["event_type"] = event_type

    if start_time is not None:
        data["start_time"] = start_time

    if end_time is not None:
        data["end_time"] = end_time

    if location is not None:
        data["location"] = location

    response = requests.patch(
        f"{BASE_URL}/events/{event_id}",
        json=data,
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def delete_event(event_id):
    response = requests.delete(
        f"{BASE_URL}/events/{event_id}",
        timeout=5
    )

    response.raise_for_status()

    if response.content:
        return response.json()

    return None


# =========================================================
# TEAMS
# =========================================================

def get_teams(event_id=None):
    params = {}

    if event_id is not None:
        params["event_id"] = event_id

    response = requests.get(
        f"{BASE_URL}/teams",
        params=params,
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def get_team(team_id):
    response = requests.get(
        f"{BASE_URL}/teams/{team_id}",
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def create_team(
    name,
    description,
    event_id,
    max_members
):
    response = requests.post(
        f"{BASE_URL}/teams",
        json={
            "name": name,
            "description": description,
            "event_id": event_id,
            "max_members": max_members
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def update_team(
    team_id,
    name=None,
    description=None,
    event_id=None,
    max_members=None
):
    data = {}

    if name is not None:
        data["name"] = name

    if description is not None:
        data["description"] = description

    if event_id is not None:
        data["event_id"] = event_id

    if max_members is not None:
        data["max_members"] = max_members

    response = requests.patch(
        f"{BASE_URL}/teams/{team_id}",
        json=data,
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def delete_team(team_id):
    response = requests.delete(
        f"{BASE_URL}/teams/{team_id}",
        timeout=5
    )

    response.raise_for_status()

    if response.content:
        return response.json()

    return None


# =========================================================
# TEAM MEMBERS
# =========================================================

def add_team_member(team_id, student_id):
    response = requests.post(
        f"{BASE_URL}/teams/{team_id}/members",
        json={
            "student_id": student_id
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def get_team_members(team_id):
    response = requests.get(
        f"{BASE_URL}/teams/{team_id}/members",
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def remove_team_member(team_id, student_id):
    response = requests.delete(
        f"{BASE_URL}/teams/{team_id}/members/{student_id}",
        timeout=5
    )

    response.raise_for_status()

    if response.content:
        return response.json()

    return None


# =========================================================
# TRANSFER LEADERSHIP
# =========================================================

def transfer_team_leadership(team_id, student_id):
    response = requests.post(
        f"{BASE_URL}/teams/{team_id}/transfer-leadership",
        json={
            "student_id": student_id
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()


# =========================================================
# STUDENT PROFILE
# =========================================================

def get_student_profile(student_id):
    response = requests.get(
        f"{BASE_URL}/students/{student_id}/profile",
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def create_student_profile(
    student_id,
    bio="",
    profile_picture="",
    github_url="",
    linkedin_url=""
):
    response = requests.post(
        f"{BASE_URL}/students/{student_id}/profile",
        json={
            "bio": bio,
            "profile_picture": profile_picture,
            "github_url": github_url,
            "linkedin_url": linkedin_url
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def update_student_profile(
    student_id,
    bio="",
    profile_picture="",
    github_url="",
    linkedin_url=""
):
    response = requests.patch(
        f"{BASE_URL}/students/{student_id}/profile",
        json={
            "bio": bio,
            "profile_picture": profile_picture,
            "github_url": github_url,
            "linkedin_url": linkedin_url
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()