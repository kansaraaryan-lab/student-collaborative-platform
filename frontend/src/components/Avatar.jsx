import React from "react";

export default function Avatar({ name = "Student", online = false }) {
  return (
    <div className="avatar-wrapper">
      <div className="avatar">
        {name.charAt(0).toUpperCase()}
      </div>

      {online && <span className="avatar-online" />}
    </div>
  );
}