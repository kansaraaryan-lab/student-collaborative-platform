import React from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  User,
  DoorOpen,
  CalendarDays,
  Users,
  MessageCircle,
  BookOpen,
  LogOut,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function AppLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigation = [
    {
      label: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      label: "Profile",
      path: "/profile",
      icon: User,
    },
    {
      label: "Room",
      path: `/room/${user?.room || "comp-a"}`,
      icon: DoorOpen,
    },
    {
      label: "Events",
      path: "/events",
      icon: CalendarDays,
    },
    {
      label: "Team Builder",
      path: "/team-builder",
      icon: Users,
    },
    {
      label: "Messages",
      path: "/messages",
      icon: MessageCircle,
    },
    {
      label: "Study Room",
      path: "/study-room",
      icon: BookOpen,
    },
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">C</div>

          <div>
            <strong>CampusConnect</strong>
            <span>Student collaboration</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navigation.map((item) => {
            const Icon = item.icon;

            const active =
              location.pathname === item.path ||
              location.pathname.startsWith(`${item.path}/`);

            return (
              <Link
                key={item.label}
                to={item.path}
                className={active ? "nav-item active" : "nav-item"}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="user-card">
            <div className="avatar">
              {user?.name?.charAt(0)?.toUpperCase() || "S"}
            </div>

            <div>
              <strong>{user?.name || "Student"}</strong>
              <span>{user?.email || "student@college.edu"}</span>
            </div>
          </div>

          <button className="logout-btn" onClick={logout}>
            <LogOut size={17} />
            Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}