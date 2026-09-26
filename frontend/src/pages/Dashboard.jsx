
import React, { useEffect, useState } from "react";
import {
  ArrowUpRight,
  CalendarDays,
  Clock3,
  MessageCircle,
  Sparkles,
  Users,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";
import SectionHeader from "../components/SectionHeader";
import Avatar from "../components/Avatar";
import api from "../api/api";

export default function Dashboard() {
  const { user } = useAuth();

  const [students, setStudents] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [skills, setSkills] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
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

        setStudents(studentsResponse.data);
        setRooms(roomsResponse.data);
        setSkills(skillsResponse.data);
        setEvents(eventsResponse.data);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      }
    };

    loadDashboardData();
  }, []);

  const studentCount = students.length;
  const roomCount = rooms.length;
  const skillCount = skills.length;
  const dashboardEvents = events
  .filter(
    (event) =>
      event.status === "upcoming" ||
      event.status === "ongoing"
  )
  .slice(0, 3);

  return (
    <>
      <SectionHeader
        title={`Good morning, ${user?.name || "Student"} 👋`}
        description={
          user?.year && user?.branch && user?.room
            ? `${user.year} · ${user.branch} · ${user.room}`
            : "Student Collaborative Platform"
        }
        action={
          <button className="primary-btn">
            Complete profile <ArrowUpRight size={17} />
          </button>
        }
      />

      <div className="stats-grid">
        <div className="stat-card accent-card">
          <div className="stat-icon">
            <Users size={19} />
          </div>

          <span>Total students</span>
          <strong>{studentCount}</strong>
          <small>Registered students</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <CalendarDays size={19} />
          </div>

          <span>Chat rooms</span>
          <strong>{roomCount}</strong>
          <small>Available chat rooms</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Sparkles size={19} />
          </div>

          <span>Skills</span>
          <strong>{skillCount}</strong>
          <small>Available skills</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Clock3 size={19} />
          </div>

          <span>Study streak</span>
          <strong>—</strong>
          <small>Coming soon</small>
        </div>
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">YOUR CHAT ROOM</p>

              <h3>{user?.room || "Your Chat Room"}</h3>
            </div>

            <a href="/room/comp-a" className="text-link">
              Open room <ArrowUpRight size={15} />
            </a>
          </div>

          <p className="muted">
            Connect with classmates, chat, and discover potential project
            teammates.
          </p>

          <div className="member-row">
            {students.slice(0, 5).map((student) => (
              <Avatar
                key={student.id}
                name={student.name || student.full_name || "Student"}
                online={false}
              />
            ))}

            {students.length > 5 && (
              <div className="more-avatar">+{students.length - 5}</div>
            )}
          </div>

          <div className="room-preview">
            <MessageCircle size={17} />

            <div>
              <strong>Room activity</strong>
              <span>Connect with your classmates</span>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">THIS WEEK</p>
              <h3>Upcoming events</h3>
            </div>

            <a href="/events" className="text-link">
              View all
            </a>
          </div>

          <div className="event-list">
          {dashboardEvents.length === 0 ? (
  <p className="muted">No upcoming events.</p>
) : (
  dashboardEvents.map((event) => {
                const date = new Date(event.start_time);

                return (
                  <div className="event-row" key={event.id}>
                    <div className="date-box">
                      <strong>{date.getDate()}</strong>

                      <span>
                        {date.toLocaleString("en-US", {
                          month: "short",
                        })}
                      </span>
                    </div>

                    <div>
                      <strong>{event.title}</strong>

                      <span>
                        {event.location || "Campus"} ·{" "}
                        {date.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                    </div>

                    <ArrowUpRight
                      size={16}
                      className="row-arrow"
                    />
                  </div>
                );
              })
            )}
          </div>
        </section>
      </div>

      <section className="panel team-banner">
        <div className="team-banner-icon">
          <Sparkles size={23} />
        </div>

        <div>
          <p className="eyebrow">TEAM BUILDER</p>

          <h3>Find teammates based on your skills</h3>

          <p className="muted">
            Find and invite classmates based on their skills and interests.
          </p>
        </div>

        <button
          className="secondary-btn"
          onClick={() => (window.location.href = "/team-builder")}
        >
          Explore matches
        </button>
      </section>
    </>
  );
}

