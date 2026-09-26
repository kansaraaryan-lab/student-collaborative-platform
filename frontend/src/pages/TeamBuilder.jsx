
import React, { useEffect, useMemo, useState } from "react";
import { Check, Filter, Search, Sparkles, Users, X } from "lucide-react";

import SectionHeader from "../components/SectionHeader";
import Avatar from "../components/Avatar";
import api from "../api/api";
import { useAuth } from "../context/AuthContext";

export default function TeamBuilder() {
  const { user } = useAuth();

  const [candidates, setCandidates] = useState([]);
  const [sentInvitations, setSentInvitations] = useState([]);
  const [invitations, setInvitations] = useState([]);

  const [search, setSearch] = useState("");
  const [skillFilter, setSkillFilter] = useState("all");

  const [loading, setLoading] = useState(true);
  const [sendingId, setSendingId] = useState(null);

  const [invitationsLoading, setInvitationsLoading] = useState(true);
  const [sentInvitationsLoading, setSentInvitationsLoading] =
    useState(true);

  const [processingInvitationId, setProcessingInvitationId] =
    useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [showFilters, setShowFilters] = useState(false);

  /*
   * Load candidates when Team Builder opens.
   */
  useEffect(() => {
    loadCandidates();
  }, []);

  /*
   * Load both received and sent invitations
   * whenever the logged-in student is available.
   */
  useEffect(() => {
    if (user?.id) {
      loadReceivedInvitations();
      loadSentInvitations();
    }
  }, [user?.id]);

  async function loadCandidates() {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/team-builder/candidates");

      setCandidates(response.data || []);
    } catch (error) {
      console.error(
        "Failed to load team candidates:",
        error
      );

      setError(
        error.response?.data?.detail ||
          "Failed to load students from the server."
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * Load invitations received by the current student.
   */
  async function loadReceivedInvitations() {
    if (!user?.id) return;

    try {
      setInvitationsLoading(true);

      const response = await api.get(
        `/team-builder/invitations/received?student_id=${user.id}`
      );

      setInvitations(response.data || []);
    } catch (error) {
      console.error(
        "Failed to load received invitations:",
        error
      );

      setError(
        error.response?.data?.detail ||
          "Failed to load received team invitations."
      );
    } finally {
      setInvitationsLoading(false);
    }
  }

  /*
   * Load invitations sent by the current student.
   *
   * This is the important part that makes invitation
   * status survive a browser refresh.
   */
  async function loadSentInvitations() {
    if (!user?.id) return;

    try {
      setSentInvitationsLoading(true);

      const response = await api.get(
        `/team-builder/invitations/sent?student_id=${user.id}`
      );

      setSentInvitations(response.data || []);
    } catch (error) {
      console.error(
        "Failed to load sent invitations:",
        error
      );

      setError(
        error.response?.data?.detail ||
          "Failed to load sent team invitations."
      );
    } finally {
      setSentInvitationsLoading(false);
    }
  }

  /*
   * Send a new invitation.
   */
  async function sendInvitation(studentId) {
    if (!user?.id) {
      setError("You are not logged in.");
      return;
    }

    if (Number(studentId) === Number(user.id)) {
      setError("You cannot invite yourself.");
      return;
    }

    /*
     * Check the actual backend-loaded invitation state.
     */
    const alreadyPending = sentInvitations.some(
      (invitation) =>
        Number(invitation.receiver_id) ===
        Number(studentId)
    );

    if (alreadyPending) {
      setError(
        "An invitation is already pending for this student."
      );
      return;
    }

    try {
      setSendingId(studentId);
      setError("");
      setSuccess("");

      const response = await api.post(
        `/team-builder/invitations?sender_id=${user.id}&receiver_id=${studentId}`
      );

      console.log(
        "Invitation sent:",
        response.data
      );

      setSuccess(
        response.data?.message ||
          "Invitation sent successfully."
      );

      /*
       * Re-fetch from backend instead of manually
       * changing the invitation state.
       */
      await loadSentInvitations();
    } catch (error) {
      console.error(
        "Failed to send invitation:",
        error
      );

      console.error(
        "Status:",
        error.response?.status
      );

      console.error(
        "Response:",
        error.response?.data
      );

      const status = error.response?.status;
      const detail = error.response?.data?.detail;

      if (status === 400) {
        setError(
          detail ||
            "Invalid invitation request."
        );
      } else if (status === 404) {
        setError(
          detail ||
            "Student was not found in the database."
        );
      } else if (status === 409) {
        setError(
          detail ||
            "An invitation is already pending."
        );

        /*
         * Backend says it already exists,
         * so synchronize our UI with the database.
         */
        await loadSentInvitations();
      } else {
        setError(
          detail ||
            "Failed to send invitation."
        );
      }
    } finally {
      setSendingId(null);
    }
  }

  /*
   * Accept or reject a received invitation.
   */
  async function updateInvitation(
    invitationId,
    status
  ) {
    try {
      setProcessingInvitationId(invitationId);
      setError("");
      setSuccess("");

      const response = await api.patch(
        `/team-builder/invitations/${invitationId}`,
        {
          status,
        }
      );

      setSuccess(
        response.data?.message ||
          `Invitation ${status}.`
      );

      /*
       * Refresh both lists after the action.
       */
      await Promise.all([
        loadReceivedInvitations(),
        loadSentInvitations(),
      ]);
    } catch (error) {
      console.error(
        "Failed to update invitation:",
        error
      );

      setError(
        error.response?.data?.detail ||
          "Failed to update invitation."
      );
    } finally {
      setProcessingInvitationId(null);
    }
  }

  /*
   * Convert sent invitations into a Set of
   * receiver IDs for fast lookup.
   */
  const sentInvitationIds = useMemo(() => {
    return new Set(
      sentInvitations.map(
        (invitation) =>
          Number(invitation.receiver_id)
      )
    );
  }, [sentInvitations]);

  /*
   * Number of pending outgoing invitations.
   */
  const selectedCount = sentInvitations.length;

  const availableSkills = useMemo(() => {
    const skills = candidates.flatMap(
      (candidate) =>
        (candidate.skills || []).map(
          (skill) => skill.name
        )
    );

    return [...new Set(skills)].sort();
  }, [candidates]);

  const filteredCandidates = useMemo(() => {
    const query = search.trim().toLowerCase();

    return candidates.filter((candidate) => {
      const matchesSearch =
        !query ||
        candidate.name
          ?.toLowerCase()
          .includes(query) ||
        candidate.college_email
          ?.toLowerCase()
          .includes(query) ||
        candidate.skills?.some((skill) =>
          skill.name
            ?.toLowerCase()
            .includes(query)
        );

      const matchesSkill =
        skillFilter === "all" ||
        candidate.skills?.some(
          (skill) =>
            skill.name?.toLowerCase() ===
            skillFilter.toLowerCase()
        );

      return (
        matchesSearch &&
        matchesSkill
      );
    });
  }, [
    candidates,
    search,
    skillFilter,
  ]);

  function clearFilters() {
    setSearch("");
    setSkillFilter("all");
  }

  return (
    <>
      <SectionHeader
        eyebrow="COLLABORATION"
        title="Team Builder"
        description="Find classmates whose skills match your project requirements."
        action={
          <button
            type="button"
            className="secondary-btn"
            onClick={() =>
              setShowFilters(!showFilters)
            }
          >
            <Filter size={17} />
            Filters
          </button>
        }
      />

      {/* Received Invitations */}
      <section
        className="panel"
        style={{ marginBottom: "20px" }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "12px",
            marginBottom: "16px",
          }}
        >
          <div>
            <span className="eyebrow">
              TEAM INVITATIONS
            </span>

            <h2
              style={{
                margin: "4px 0 0",
              }}
            >
              Received Invitations
            </h2>
          </div>

          {invitations.length > 0 && (
            <span className="tag">
              {invitations.length} pending
            </span>
          )}
        </div>

        {invitationsLoading ? (
          <p className="muted">
            Loading invitations...
          </p>
        ) : invitations.length === 0 ? (
          <p className="muted">
            No pending team invitations.
          </p>
        ) : (
          <div
            style={{
              display: "grid",
              gap: "12px",
            }}
          >
            {invitations.map(
              (invitation) => {
                const isProcessing =
                  processingInvitationId ===
                  invitation.invitation_id;

                return (
                  <article
                    key={
                      invitation.invitation_id
                    }
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent:
                        "space-between",
                      gap: "16px",
                      flexWrap: "wrap",
                      padding: "14px",
                      border:
                        "1px solid var(--border, #ddd)",
                      borderRadius: "12px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <Avatar
                        name={
                          invitation.sender_name ||
                          "Student"
                        }
                        online
                      />

                      <div>
                        <strong>
                          {
                            invitation.sender_name
                          }
                        </strong>

                        <p
                          className="muted"
                          style={{
                            margin:
                              "3px 0 0",
                          }}
                        >
                          {
                            invitation.sender_email
                          }
                        </p>

                        <small className="muted">
                          Invited you to join
                          their team
                        </small>
                      </div>
                    </div>

                    <div
                      style={{
                        display: "flex",
                        gap: "8px",
                      }}
                    >
                      <button
                        type="button"
                        className="primary-btn"
                        disabled={
                          isProcessing
                        }
                        onClick={() =>
                          updateInvitation(
                            invitation.invitation_id,
                            "accepted"
                          )
                        }
                      >
                        <Check size={16} />

                        {isProcessing
                          ? "Processing..."
                          : "Accept"}
                      </button>

                      <button
                        type="button"
                        className="secondary-btn"
                        disabled={
                          isProcessing
                        }
                        onClick={() =>
                          updateInvitation(
                            invitation.invitation_id,
                            "rejected"
                          )
                        }
                      >
                        <X size={16} />
                        Reject
                      </button>
                    </div>
                  </article>
                );
              }
            )}
          </div>
        )}
      </section>

      <section className="project-brief panel">
        <div className="project-brief-icon">
          <Sparkles size={22} />
        </div>

        <div className="project-brief-main">
          <span className="eyebrow">
            ACTIVE ASSIGNMENT
          </span>

          <h2>
            Smart Campus Management
          </h2>

          <p className="muted">
            Build a platform that improves
            student access to campus
            services.
          </p>

          <div className="tag-list">
            <span className="tag">
              Python
            </span>

            <span className="tag">
              SQL
            </span>

            <span className="tag">
              ML
            </span>

            <span className="tag">
              Frontend
            </span>
          </div>
        </div>

        <div className="team-size">
          <span>Pending invitations</span>

          <strong>
            {selectedCount} / 4
          </strong>

          <small>
            teammates invited
          </small>
        </div>
      </section>

      <div className="team-toolbar">
        <div className="search-field">
          <Search size={17} />

          <input
            type="text"
            placeholder="Search by name or skill..."
            value={search}
            onChange={(event) => {
              setSearch(event.target.value);
              setError("");
            }}
          />
        </div>

        <span className="match-note">
          Showing students from the college
          database
        </span>
      </div>

      {showFilters && (
        <div
          className="panel"
          style={{
            marginBottom: "20px",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >
            <strong>
              Filter by skill:
            </strong>

            <select
              value={skillFilter}
              onChange={(event) =>
                setSkillFilter(
                  event.target.value
                )
              }
            >
              <option value="all">
                All skills
              </option>

              {availableSkills.map(
                (skill) => (
                  <option
                    key={skill}
                    value={skill}
                  >
                    {skill}
                  </option>
                )
              )}
            </select>

            {(search ||
              skillFilter !== "all") && (
              <button
                type="button"
                className="secondary-btn"
                onClick={
                  clearFilters
                }
              >
                Clear
              </button>
            )}
          </div>
        </div>
      )}

      {error && (
        <div
          className="panel"
          style={{
            marginBottom: "20px",
          }}
        >
          <strong>
            Team Builder Error
          </strong>

          <p>{error}</p>
        </div>
      )}

      {success && (
        <div
          className="panel"
          style={{
            marginBottom: "20px",
          }}
        >
          <strong>
            ✓ {success}
          </strong>
        </div>
      )}

      {loading ||
      sentInvitationsLoading ? (
        <div className="panel">
          Loading team data...
        </div>
      ) : filteredCandidates.length ===
        0 ? (
        <div className="panel">
          <strong>
            No students found.
          </strong>

          <p className="muted">
            Try another name, email,
            or skill.
          </p>
        </div>
      ) : (
        <div className="candidate-grid">
          {filteredCandidates.map(
            (candidate) => {
              const studentId =
                candidate.student_id;

              /*
               * IMPORTANT:
               * This now comes from the backend.
               * It survives browser refresh.
               */
              const isPending =
                sentInvitationIds.has(
                  Number(studentId)
                );

              const isSending =
                sendingId === studentId;

              const isCurrentUser =
                Number(studentId) ===
                Number(user?.id);

              const skills =
                candidate.skills || [];

              return (
                <article
                  className={`candidate-card panel ${
                    isPending
                      ? "selected"
                      : ""
                  }`}
                  key={studentId}
                >
                  <div className="candidate-top">
                    <Avatar
                      name={
                        candidate.name ||
                        "Student"
                      }
                      online
                    />

                    <div>
                      <h3>
                        {candidate.name}
                      </h3>

                      <span>
                        {
                          candidate.college_email
                        }
                      </span>
                    </div>
                  </div>

                  <div className="tag-list">
                    {skills.length >
                    0 ? (
                      skills.map(
                        (
                          skill,
                          index
                        ) => (
                          <span
                            className="tag"
                            key={`${studentId}-${skill.name}-${index}`}
                          >
                            {skill.name}

                            {skill.proficiency && (
                              <>
                                {" · "}
                                {
                                  skill.proficiency
                                }
                              </>
                            )}
                          </span>
                        )
                      )
                    ) : (
                      <span className="muted">
                        No skills added
                        yet.
                      </span>
                    )}
                  </div>

                  <button
                    type="button"
                    className={
                      isPending
                        ? "primary-btn full"
                        : "secondary-btn full"
                    }
                    disabled={
                      isSending ||
                      isPending ||
                      isCurrentUser
                    }
                    onClick={() =>
                      sendInvitation(
                        studentId
                      )
                    }
                  >
                    {isSending ? (
                      <>
                        <Users size={16} />
                        Sending...
                      </>
                    ) : isPending ? (
                      <>
                        <Check size={16} />
                        Invitation Pending
                      </>
                    ) : isCurrentUser ? (
                      <>
                        <Users size={16} />
                        You
                      </>
                    ) : selectedCount >=
                      4 ? (
                      <>
                        <Users size={16} />
                        Team Full
                      </>
                    ) : (
                      <>
                        <Users size={16} />
                        Invite to Team
                      </>
                    )}
                  </button>
                </article>
              );
            }
          )}
        </div>
      )}
    </>
  );
}
