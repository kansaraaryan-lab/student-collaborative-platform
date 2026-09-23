
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"


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

#Events
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


# =========================================================
# TEAMS
# =========================================================

def get_teams(event_id=None):
    params = {}

    if event_id:
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
    created_by
):
    response = requests.post(
        f"{BASE_URL}/teams",
        json={
            "name": name,
            "description": description,
            "event_id": event_id,
            "created_by": created_by
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def add_team_member(
    team_id,
    student_id
):
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


def remove_team_member(
    team_id,
    student_id
):
    response = requests.delete(
        f"{BASE_URL}/teams/{team_id}/members/{student_id}",
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


def create_student_profile(student_id, bio="", github="", linkedin="", portfolio=""):
    response = requests.post(
        f"{BASE_URL}/students/{student_id}/profile",
        json={
            "bio": bio,
            "github": github,
            "linkedin": linkedin,
            "portfolio": portfolio
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def update_student_profile(student_id, bio="", github="", linkedin="", portfolio=""):
    response = requests.patch(
        f"{BASE_URL}/students/{student_id}/profile",
        json={
            "bio": bio,
            "github": github,
            "linkedin": linkedin,
            "portfolio": portfolio
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()

# =========================
# STUDENT PROFILE
# =========================

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