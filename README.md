# Student Collaborative Platform

A secure, full-stack collaboration platform designed for engineering college students to connect with classmates, manage profiles and skills, discover teammates, participate in events, and communicate with other students.

The project is built using a React frontend, Python FastAPI backend, and PostgreSQL database, with a focus on modular architecture, database integrity, authentication, authorization, and secure API design.

---

## 📌 Project Overview

The Student Collaborative Platform provides a centralized environment where students can:

- Create and manage their student profiles
- View classmates from their academic room
- Add and manage technical skills
- Discover other students based on skills and academic information
- Create and join teams
- Send and receive team invitations
- Create and manage events
- Communicate with other students through messaging
- Use real-time messaging through WebSockets
- Authenticate using their college Google account

The system follows a client-server architecture where the React frontend communicates with the FastAPI backend, while the backend manages business logic, authentication, database operations, and security.

---

## 🎯 Objectives

The main objectives of the project are:

1. Provide a centralized platform for student collaboration.
2. Help students discover classmates and potential teammates.
3. Allow students to showcase their skills and academic information.
4. Simplify team formation for academic and extracurricular activities.
5. Provide an event management system.
6. Enable student-to-student communication.
7. Implement authentication and role-based authorization.
8. Maintain a structured and relational PostgreSQL database.
9. Follow a modular and maintainable full-stack architecture.
10. Apply security principles throughout the application.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        Student       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React + Vite       │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                         HTTP / REST
                         WebSocket
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Authentication       Business          Validation
       & RBAC              Logic             / Schemas
             │                 │                 │  
             └─────────────────┤─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │     SQLAlchemy       │
                    │         ORM          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │       Database       │
                    └──────────────────────┘
```

Database schema changes are managed using **Alembic migrations**.

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- JavaScript
- React Router
- WebSocket client
- Context-based application state

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Uvicorn
- Google Authentication libraries

### Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations

### Development & Infrastructure

- Docker
- Docker Desktop
- Git
- GitHub
- Visual Studio Code
- Python virtual environment
- Swagger / OpenAPI

---

## ✨ Main Features

### 🔐 Authentication & Authorization

The platform integrates Google-based authentication for student login.

The backend handles:

- Google credential verification
- Authentication
- Authorization
- Role-based access control
- Protected API operations

Administrative privileges are supported through the `is_admin` field.

---

### 👤 Student Profiles

Students can maintain their academic and personal profile information.

Profile information includes:

- Student name
- College email
- Year
- Branch
- Bio
- GitHub profile
- LinkedIn profile
- Skills

The frontend provides an interface for viewing and updating profile information through backend APIs.

---

### 🏫 Academic Rooms

Students are organized into academic rooms based on their academic information.

Rooms contain information such as:

- Year
- Branch
- Division

Students can view classmates associated with their academic room.

---

### 🧠 Skills Management

Students can associate technical skills with their profiles.

The system uses a many-to-many relationship:

```text
Student
   │
   ▼
student_skills
   │
   ▼
Skill
```

This allows multiple students to have the same skill while allowing each student to have multiple skills.

---

### 👥 Team Builder

The Team Builder allows students to collaborate and form teams.

Features include:

- Discover potential teammates
- Create teams
- View current team
- Team membership
- Send invitations
- Receive invitations
- Accept or reject invitations

The database enforces constraints to maintain team membership integrity.

---

### 📅 Events

The Events module allows students to interact with academic or campus events.

Supported operations include:

- View events
- Create events
- Update events
- Delete events
- View events according to their status

---

### 💬 Messaging

Students can communicate directly with one another.

The messaging system supports:

- Sending messages
- Retrieving conversations
- Sender/receiver relationships
- Real-time communication through WebSockets

The backend provides both REST API functionality and WebSocket support.

---

## 🗄️ Database Design

The current PostgreSQL database contains the following application tables:

```text
students
student_profiles
rooms
skills
student_skills
events
teams
team_members
team_invitations
messages
```

Alembic additionally maintains:

```text
alembic_version
```

which tracks the current database migration revision.

### Core Relationships

```text
students
   │
   ├──────── student_profiles
   │
   ├──────── rooms
   │
   ├──────── student_skills ───── skills
   │
   ├──────── team_members ─────── teams
   │
   ├──────── team_invitations
   │
   ├──────── messages
   │
   └──────── events
```

The database uses primary keys, foreign keys, unique constraints, and other relational constraints to maintain data integrity.

---

## 🔌 API

The backend exposes REST APIs under:

```text
/api/v1
```

### Health

```text
GET /api/v1/health
```

### Rooms

```text
GET    /api/v1/rooms
POST   /api/v1/rooms
GET    /api/v1/rooms/{room_id}
PATCH  /api/v1/rooms/{room_id}
DELETE /api/v1/rooms/{room_id}
```

### Students

```text
GET    /api/v1/students
POST   /api/v1/students
GET    /api/v1/students/{student_id}
PATCH  /api/v1/students/{student_id}
DELETE /api/v1/students/{student_id}
```

### Student Profiles

```text
POST  /api/v1/students/{student_id}/profile
GET   /api/v1/students/{student_id}/profile
PATCH /api/v1/students/{student_id}/profile
```

### Skills

```text
GET    /api/v1/skills
POST   /api/v1/skills
GET    /api/v1/skills/{skill_id}
PATCH  /api/v1/skills/{skill_id}
DELETE /api/v1/skills/{skill_id}
```

### Student Skills

```text
POST   /api/v1/student-skills
GET    /api/v1/students/{student_id}/skills
DELETE /api/v1/students/{student_id}/skills/{skill_id}
```

### Authentication

```text
POST /api/v1/auth/google
```

### Messaging

```text
GET  /api/v1/messages/{student_id}
POST /api/v1/messages
```

### Team Builder

```text
GET   /api/v1/team-builder/candidates
POST  /api/v1/team-builder/teams
POST  /api/v1/team-builder/invitations
GET   /api/v1/team-builder/invitations/received
PATCH /api/v1/team-builder/invitations/{invitation_id}
GET   /api/v1/team-builder/invitations/sent
GET   /api/v1/team-builder/my-team
```

### Events

```text
GET    /api/v1/events
POST   /api/v1/events
PATCH  /api/v1/events/{event_id}
DELETE /api/v1/events/{event_id}
```

---

## 📖 API Documentation

FastAPI automatically generates interactive API documentation using OpenAPI.

After starting the backend, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```text
Student-Collaborative-Platform/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependency.py
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── events.py
│   │   │       ├── messages.py
│   │   │       ├── messages_ws.py
│   │   │       ├── rooms.py
│   │   │       ├── skills.py
│   │   │       ├── student_profiles.py
│   │   │       ├── student_skills.py
│   │   │       ├── students.py
│   │   │       ├── team_builder.py
│   │   │       └── router.py
│   │   │
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── scripts/
│   │   └── seed_demo_data.py
│   │
│   └── ...
│
├── alembic/
│   └── versions/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   │
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔒 Security Considerations

Security is treated as a core requirement of the project.

The application incorporates security mechanisms including:

- Google-based authentication
- Role-Based Access Control (RBAC)
- Backend-side authorization
- Pydantic request validation
- SQLAlchemy ORM for database interaction
- PostgreSQL foreign-key constraints
- Unique constraints
- Protected frontend routes
- Environment-based configuration
- Separation of frontend and database access
- WebSocket-based communication through the backend

The application is structured so that the frontend does not directly communicate with the PostgreSQL database.

---

## 🚀 Local Development Setup

### Prerequisites

Install:

- Python 3.13+
- Node.js and npm
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/kansaraaryan-lab/student-collaborative-platform.git
cd student-collaborative-platform
```

### 2. Create and activate Python virtual environment

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=platform_user
POSTGRES_PASSWORD=platform_password
POSTGRES_DB=student_platform

GOOGLE_CLIENT_ID=your_google_client_id
```

Do not commit real credentials or secrets to Git.

### 5. Start PostgreSQL

Start the PostgreSQL development database using Docker.

The backend connects to:

```text
localhost:5432
```

### 6. Apply database migrations

```powershell
alembic upgrade head
```

### 7. Start the FastAPI backend

```powershell
uvicorn backend.app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 8. Start the React frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## 🌱 Development Data

The project contains a development/demo data script:

```text
backend/scripts/seed_demo_data.py
```

It is intended to populate the local development database with sample application data.

---

## 🧪 Testing

The application can be tested at multiple levels:

### Backend

- API endpoint testing
- Request validation
- Authentication and authorization testing
- Database constraint testing

### Frontend

- Page and navigation testing
- API integration testing
- Authentication flow testing
- User interaction testing

### API Documentation

Swagger/OpenAPI provides an interactive interface for testing backend endpoints during development.

---

## 🔄 Database Migrations

Alembic is used to manage database schema changes.

Migration workflow:

```text
SQLAlchemy Models
       ↓
Alembic Migration
       ↓
PostgreSQL Schema
```

Migration history includes changes for:

- Core tables
- Rooms
- Skills
- Messages
- Team invitations
- Teams and team members
- Admin support
- Student year/branch
- Team membership constraints
- Events

---

## 👨‍💻 Development Team

### Backend & Cybersecurity

Responsible for:

- FastAPI backend
- PostgreSQL integration
- API development
- Database design
- Authentication and authorization
- Security implementation

### Frontend

Responsible for:

- React application
- User interface
- Navigation
- API integration
- User experience

### Research / UX / Features

Responsible for:

- Feature research
- User requirements
- UX considerations
- Project functionality

### QA / Data Structures / Documentation

Responsible for:

- Testing
- Data structure considerations
- Documentation
- Project presentation

---

## 📌 Project Status

The current application includes:

- [x] React frontend
- [x] FastAPI backend
- [x] PostgreSQL database
- [x] Alembic migrations
- [x] Student management
- [x] Student profiles
- [x] Academic rooms
- [x] Skills management
- [x] Team Builder
- [x] Team invitations
- [x] Events
- [x] Messaging
- [x] WebSocket messaging support
- [x] Google authentication integration
- [x] RBAC integration
- [x] Swagger/OpenAPI documentation

Further development can focus on additional testing, production hardening, deployment, and feature refinement.

---

## 📄 Project Information

This project was developed as a B.Tech academic project by the Student Collaborative Platform team.

## 📄 License

MIT License.
