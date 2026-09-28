import { useEffect, useState } from "react";
import {
  ArrowUpRight,
  CalendarDays,
  MessageCircle,
  Sparkles,
  Users,
  UserRound,
  GraduationCap,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/useAuth";
import SectionHeader from "../components/SectionHeader";
import Avatar from "../components/Avatar";
import api from "../api/api";

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [students, setStudents] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [skills, setSkills] = useState([]);
  const [events, setEvents] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);

        const [
          studentsResponse,
          roomsResponse,
          skillsResponse,
          eventsResponse,
        ] = await Promise.all([
          api.get("/students"),
          api.get("/rooms"),
          api.get("/skills"),
          api.get("/events"),
        ]);

        setStudents(studentsResponse.data || []);
        setRooms(roomsResponse.data || []);
        setSkills(skillsResponse.data || []);
        setEvents(eventsResponse.data || []);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const hour = new Date().getHours();

  let greeting = "Good evening";

  if (hour < 12) {
    greeting = "Good morning";
  } else if (hour < 17) {
    greeting = "Good afternoon";
  }

  const currentRoomId = user?.roomId;

  const classmates = students.filter(
    (student) =>
      Number(student.room_id) === Number(currentRoomId) &&
      Number(student.id) !== Number(user?.id)
  );

  const currentRoom = rooms.find(
    (room) => Number(room.id) === Number(currentRoomId)
  );

  const roomName =
    currentRoom?.name ||
    currentRoom?.room_name ||
    currentRoom?.title ||
    "Your Class";

  const upcomingEvents = events
    .filter(
      (event) =>
        event.status === "upcoming" ||
        event.status === "ongoing"
    )
    .sort(
      (a, b) =>
        new Date(a.start_time) - new Date(b.start_time)
    )
    .slice(0, 3);

  const studentCount = students.length;
  const roomCount = rooms.length;
  const skillCount = skills.length;

  const formatDate = (dateString) => {
    const date = new Date(dateString);

    return {
      day: date.getDate(),
      month: date.toLocaleString("en-US", {
        month: "short",
      }),
      time: date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };
  };

  return (
    <>
      <SectionHeader
        eyebrow="STUDENT DASHBOARD"
        title={`${greeting}, ${user?.name || "Student"} 👋`}
        description="Your central workspace for classes, teammates, skills, messages, and events."
        action={
          <button
            className="primary-btn"
            onClick={() => navigate("/profile")}
          >
            View profile
            <ArrowUpRight size={17} />
          </button>
        }
      />

      <div className="stats-grid">
        <div className="stat-card accent-card">
          <div className="stat-icon">
            <Users size={19} />
          </div>

          <span>Classmates</span>

          <strong>{loading ? "—" : classmates.length}</strong>

          <small>Students in your class</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <CalendarDays size={19} />
          </div>

          <span>Upcoming events</span>

          <strong>
            {loading ? "—" : upcomingEvents.length}
          </strong>

          <small>Events on your calendar</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Sparkles size={19} />
          </div>

          <span>Available skills</span>

          <strong>{loading ? "—" : skillCount}</strong>

          <small>Skills for team discovery</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <GraduationCap size={19} />
          </div>

          <span>Academic rooms</span>

          <strong>{loading ? "—" : roomCount}</strong>

          <small>Available class spaces</small>
        </div>
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">MY CLASS</p>
              <h3>{roomName}</h3>
            </div>
            <button
              className="text-link"
              onClick={() => navigate(`/room/${currentRoomId}`)}
            >
              Open class
              <ArrowUpRight size={15} />
            </button>
          </div>

          <p className="muted">
            Connect with your classmates and discover
            potential teammates for your projects.
          </p>

          <div className="member-row">
            {classmates.slice(0, 5).map((student) => (
              <Avatar
                key={student.id}
                name={student.name || "Student"}
                online={false}
              />
            ))}

            {classmates.length > 5 && (
              <div className="more-avatar">
                +{classmates.length - 5}
              </div>
            )}

            {classmates.length === 0 && (
              <span className="muted">
                No classmates found.
              </span>
            )}
          </div>

          <div className="room-preview">
            <Users size={17} />

            <div>
              <strong>
                {classmates.length} classmates
              </strong>

              <span>
                Explore your academic community
              </span>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">CAMPUS CALENDAR</p>
              <h3>Upcoming events</h3>
            </div>

            <button
              className="text-link"
              onClick={() => navigate("/events")}
            >
              View all
              <ArrowUpRight size={15} />
            </button>
          </div>

          <div className="event-list">
            {loading && (
              <p className="muted">
                Loading events...
              </p>
            )}

            {!loading && upcomingEvents.length === 0 && (
              <p className="muted">
                No upcoming events right now.
              </p>
            )}

            {!loading &&
              upcomingEvents.map((event) => {
                const eventDate = formatDate(
                  event.start_time
                );

                return (
                  <div
                    className="event-row"
                    key={event.id}
                  >
                    <div className="date-box">
                      <strong>{eventDate.day}</strong>

                      <span>{eventDate.month}</span>
                    </div>

                    <div>
                      <strong>{event.title}</strong>

                      <span>
                        {event.location || "Campus"} ·{" "}
                        {eventDate.time}
                      </span>
                    </div>

                    <span className="event-status">
                      {event.status === "ongoing"
                        ? "Ongoing"
                        : "Upcoming"}
                    </span>
                  </div>
                );
              })}
          </div>
        </section>
      </div>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">QUICK ACTIONS</p>
            <h3>What would you like to do?</h3>
          </div>
        </div>

        <div className="dashboard-actions">
          <button
            className="dashboard-action"
            onClick={() => navigate("/profile")}
          >
            <UserRound size={20} />

            <div>
              <strong>My Profile</strong>
              <span>
                View and update your student profile
              </span>
            </div>

            <ArrowUpRight size={16} />
          </button>

          <button
            className="dashboard-action"
            onClick={() => navigate("/messages")}
          >
            <MessageCircle size={20} />

            <div>
              <strong>Messages</strong>
              <span>
                Connect with your classmates
              </span>
            </div>

            <ArrowUpRight size={16} />
          </button>

          <button
            className="dashboard-action"
            onClick={() => navigate("/team-builder")}
          >
            <Users size={20} />

            <div>
              <strong>Team Builder</strong>
              <span>
                Find teammates based on skills
              </span>
            </div>

            <ArrowUpRight size={16} />
          </button>
        </div>
      </section>

      <section className="panel team-banner">
        <div className="team-banner-icon">
          <Sparkles size={23} />
        </div>

        <div>
          <p className="eyebrow">TEAM BUILDER</p>

          <h3>Build your next project team</h3>

          <p className="muted">
            Find classmates with complementary technical
            skills and send them an invitation.
          </p>
        </div>

        <button
          className="secondary-btn"
          onClick={() => navigate("/team-builder")}
        >
          Find teammates
        </button>
      </section>
    </>
  );
}
