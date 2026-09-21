from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import engine

from backend.app.models.room import Room
from backend.app.models.student import Student
from backend.app.models.student_profile import StudentProfile
from backend.app.models.skill import Skill
from backend.app.models.student_skill import StudentSkill


def seed_demo_data():
    with Session(engine) as db:
        try:
            # ---------------------------------------------------------
            # 1. Rooms
            # ---------------------------------------------------------

            room_year2 = db.scalar(
                select(Room).where(
                    Room.year == 2,
                    Room.branch == "Computer Engineering",
                    Room.division == "A",
                )
            )

            if room_year2 is None:
                room_year2 = Room(
                    year=2,
                    branch="Computer Engineering",
                    division="A",
                )
                db.add(room_year2)
                db.flush()

            room_year1 = db.scalar(
                select(Room).where(
                    Room.year == 1,
                    Room.branch.is_(None),
                    Room.division == "A",
                )
            )

            if room_year1 is None:
                room_year1 = Room(
                    year=1,
                    branch=None,
                    division="A",
                )
                db.add(room_year1)
                db.flush()

            # ---------------------------------------------------------
            # 2. Demo student
            # ---------------------------------------------------------

            demo_email = "124aryan2111@sjcem.trial.demo"

            student = db.scalar(
                select(Student).where(
                    Student.college_email == demo_email
                )
            )

            if student is None:
                student = Student(
                    college_email=demo_email,
                    name="Aryan Kansara(Demo)",
                    room_id=room_year2.id,
                )
                db.add(student)
                db.flush()

            # ---------------------------------------------------------
            # 3. Student profile
            # ---------------------------------------------------------

            profile = db.scalar(
                select(StudentProfile).where(
                    StudentProfile.student_id == student.id
                )
            )

            if profile is None:
                profile = StudentProfile(
                    student_id=student.id,
                    bio=(
                        "[DEMO] Computer engineering student interested "
                        "in cybersecurity and software development."
                    ),
                    profile_picture="https://example.com/profile.jpg",
                    github_url="https://github.com/example",
                    linkedin_url="https://linkedin.com/in/example",
                )
                db.add(profile)

            # ---------------------------------------------------------
            # 4. Skills
            # ---------------------------------------------------------

            skill_names = [
                "Python",
                "JavaScript",
                "React",
                "PostgreSQL",
                "FastAPI",
                "Cybersecurity",
                "Web Security",
                "Docker",
                "Linux",
                "Machine Learning",
            ]

            skills = {}

            for skill_name in skill_names:
                skill = db.scalar(
                    select(Skill).where(
                        Skill.name == skill_name
                    )
                )

                if skill is None:
                    skill = Skill(name=skill_name)
                    db.add(skill)
                    db.flush()

                skills[skill_name] = skill

            # ---------------------------------------------------------
            # 5. Student skills
            # ---------------------------------------------------------

            student_skill_data = {
                "Python": "Beginner",
                "Cybersecurity": "Intermediate",
                "Web Security": "Intermediate",
            }

            for skill_name, proficiency in student_skill_data.items():
                existing = db.scalar(
                    select(StudentSkill).where(
                        StudentSkill.student_id == student.id,
                        StudentSkill.skill_id == skills[skill_name].id,
                    )
                )

                if existing is None:
                    db.add(
                        StudentSkill(
                            student_id=student.id,
                            skill_id=skills[skill_name].id,
                            proficiency=proficiency,
                        )
                    )

            db.commit()

            print("Demo data seeded successfully.")
            print(f"Demo student ID: {student.id}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    seed_demo_data()