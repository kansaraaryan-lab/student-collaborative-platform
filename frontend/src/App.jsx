import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import AppLayout from "./components/AppLayout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Room from "./pages/Room";
import Events from "./pages/Events";
import TeamBuilder from "./pages/TeamBuilder";
import Messages from "./pages/Messages";
import StudyRoom from "./pages/StudyRoom";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/profile/:id" element={<Profile />} />
          <Route path="/room/:roomId" element={<Room />} />
          <Route path="/events" element={<Events />} />
          <Route path="/team-builder" element={<TeamBuilder />} />
          <Route path="/messages" element={<Messages />} />
        {/* <Route path="/study-room" element={<StudyRoom />} /> */}
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

