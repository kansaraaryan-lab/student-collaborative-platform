import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  CheckCircle2,
  ShieldCheck,
  Users,
  CalendarDays,
} from "lucide-react";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const googleButtonRef = useRef(null);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const initializeGoogle = () => {
      if (!window.google || !googleButtonRef.current) {
        return;
      }

      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,

        callback: async (response) => {
          setError("");
          setLoading(true);

          try {
            const result = await login(response.credential);

            if (result.success) {
              navigate("/dashboard", { replace: true });
            } else {
              setError(result.error);
            }
          } catch (err) {
            console.error("Google login failed:", err);
            setError("Google login failed. Please try again.");
          } finally {
            setLoading(false);
          }
        },
      });

      googleButtonRef.current.innerHTML = "";

      window.google.accounts.id.renderButton(
        googleButtonRef.current,
        {
          type: "standard",
          theme: "outline",
          size: "large",
          text: "continue_with",
          shape: "rectangular",
          width: 320,
        }
      );
    };

    if (window.google) {
      initializeGoogle();
    } else {
      window.onGoogleLibraryLoad = initializeGoogle;
    }

    return () => {
      window.onGoogleLibraryLoad = null;
    };
  }, [login, navigate]);

  return (
    <div className="login-page">
      <div className="login-visual">
        <div className="visual-glow glow-one" />
        <div className="visual-glow glow-two" />

        <div className="visual-content">
          <div className="brand brand-light">
            <div className="brand-mark">C</div>

            <div>
              <strong>CampusConnect</strong>
              <span>Student collaboration</span>
            </div>
          </div>

          <div className="hero-copy">
            <span className="kicker">YOUR CAMPUS. ONE PLACE.</span>

            <h1>
              Find your people.
              <br />
              <em>Build something great.</em>
            </h1>

            <p>
              Connect with classmates, discover events, build project teams,
              and study together inside your college community.
            </p>
          </div>

          <div className="feature-strip">
            <span>
              <Users size={16} /> Student network
            </span>

            <span>
              <CalendarDays size={16} /> College events
            </span>

            <span>
              <ShieldCheck size={16} /> College verified
            </span>
          </div>
        </div>
      </div>

      <div className="login-panel">
        <div className="login-card">
          <div className="mobile-brand brand">
            <div className="brand-mark">C</div>

            <div>
              <strong>CampusConnect</strong>
              <span>Student collaboration</span>
            </div>
          </div>

          <span className="eyebrow">WELCOME BACK</span>

          <h2>Sign in to your campus</h2>

          <p className="muted">
            Use your college Google account to access your academic community.
          </p>

          <div
            ref={googleButtonRef}
            style={{
              minHeight: "44px",
              display: "flex",
              justifyContent: "center",
              marginTop: "20px",
              marginBottom: "12px",
            }}
          />

          {loading && (
            <div className="login-loading">
              Signing in...
            </div>
          )}

          {error && (
            <div className="login-error">
              {error}
            </div>
          )}

          <div className="verified-note">
            <CheckCircle2 size={17} />

            <span>
              Only verified @sjcem.edu.in accounts are allowed.
            </span>
          </div>

          <div className="login-footer">
            <span>Secure login</span>
            <span>·</span>
            <span>Google OAuth</span>
          </div>
        </div>
      </div>
    </div>
  );
}

