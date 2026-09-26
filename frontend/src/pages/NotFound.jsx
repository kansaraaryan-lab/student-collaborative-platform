import React from "react";
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="not-found">
      <h1>404</h1>
      <h2>Page not found</h2>
      <p className="muted">
        The page you are looking for does not exist.
      </p>

      <Link to="/dashboard" className="primary-btn">
        Go to Dashboard
      </Link>
    </div>
  );
}