import React, { useEffect, useMemo, useState } from "react";
import {
  Check,
  Filter,
  Search,
  Sparkles,
  Users,
  X,
} from "lucide-react";

import SectionHeader from "../components/SectionHeader";
import Avatar from "../components/Avatar";
import api from "../api/api";
import { useAuth } from "../context/AuthContext";

export default function TeamBuilder() {
  const { user } = useAuth();

  const [candidates, setCandidates] = useState([]);
  const [sentInvitations, setSentInvitations] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [myTeam, setMyTeam] = useState(null);

  const [search, setSearch] = useState("");
  const [skillFilter, setSkillFilter] = useState("all");

  const [loading, setLoading] = useState(true);
  const [sendingId, setSendingId] = useState(null);

  const [invitationsLoading, setInvitationsLoading] =
    useState(true);

  const [sentInvitationsLoading, setSentInvitationsLoading] =
    useState(true);

  const [teamLoading, setTeamLoading] = useState(true);
  const [creatingTeam, setCreatingTeam] = useState(false);

  const [teamName, setTeamName] = useState("");
  const [showCreateTeam, setShowCreateTeam] = useState(false);

  const [processingInvitationId, setProcessingInvitationId] =
    useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [showFilters, setShowFilters] = useState(false);

  // Load candidates
  useEffect(() => {
    loadCandidates();
  }, []);

  // Load team and invitations
  useEffect(() => {
    if (user?.id) {
      loadMyTeam();
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
      console.error("Failed to load team candidates:", error);

      setError(
        error.response?.data?.detail ||
          "Failed to load students from the server."
      );
    } finally {
      setLoading(false);
    }
  }

  // Load current student's team
  async function loadMyTeam() {
    if (!user?.id) return;

    try {
      setTeamLoading(true);

      const response = await api.get(
        `/team-builder/my-team?student_id=${user.id}`
      );

      if (response.data?.team) {
        setMyTeam(response.data);
        setShowCreateTeam(false);
      } else {
        setMyTeam(null);
      }
    } catch (error) {
      console.error("Failed to load current team:", error);

      setError(
        error.response?.data?.detail ||
          "Failed to load your team."
      );
    } finally {
      setTeamLoading(false);
    }
  }

  // Create a new team
  async function createTeam() {
    const name = teamName.trim();

    if (!user?.id) {
      setError("You are not logged in.");
      return;
    }

    if (!name) {
      setError("Please enter a team name.");
      return;
    }

    try {
      setCreatingTeam(true);
      setError("");
      setSuccess("");

      const response = await api.post(
        `/team-builder/teams?student_id=${user.id}`,
        {
          name,
        }
      );

      setSuccess(
        response.data?.message ||
          "Team created successfully."
      );

      setTeamName("");
      setShowCreateTeam(false);

      await loadMyTeam();
    } catch (error) {
      console.error("Failed to create team:", error);

      setError(
        error.response?.data?.detail ||
          "Failed to create team."
      );
    } finally {
      setCreatingTeam(false);
    }
  }

  // Load received invitations
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

  // Load sent invitations
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

  // Send invitation
  async function sendInvitation(studentId) {
    if (!user?.id) {
      setError("You are not logged in.");
      return;
    }

    if (!myTeam?.team) {
      setError(
        "Create a team before inviting teammates."
      );
      return;
    }

    if (Number(studentId) === Number(user.id)) {
      setError("You cannot invite yourself.");
      return;
    }

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

      console.log("Invitation sent:", response.data);

      setSuccess(
        response.data?.message ||
          "Invitation sent successfully."
      );

      await loadSentInvitations();
    } catch (error) {
      console.error("Failed to send invitation:", error);

      const status = error.response?.status;
      const detail = error.response?.data?.detail;

      if (status === 400) {
        setError(
          detail || "Invalid invitation request."
        );
      } else if (status === 404) {
        setError(
          detail ||
            "Student was not found in the database."
        );
      } else if (status === 409) {
        setError(
          detail || "Unable to send invitation."
        );

        await loadSentInvitations();
      } else {
        setError(
          detail || "Failed to send invitation."
        );
      }
    } finally {
      setSendingId(null);
    }
  }

  // Accept or reject invitation
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

      await Promise.all([
        loadMyTeam(),
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

  // Pending invitation IDs
  const sentInvitationIds = useMemo(() => {
    return new Set(
      sentInvitations.map(
        (invitation) =>
          Number(invitation.receiver_id)
      )
    );
  }, [sentInvitations]);

  // Pending outgoing invitations
  const pendingInvitationCount =
    sentInvitations.length;

  // Actual team members
  const teamMemberCount =
    myTeam?.members?.length || 0;

  // Available skills
  const availableSkills = useMemo(() => {
    const skills = candidates.flatMap(
      (candidate) =>
        (candidate.skills || []).map(
          (skill) => skill.name
        )
    );

    return [...new Set(skills)].sort();
  }, [candidates]);

  // Filter candidates
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

      {/* My Team */}
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
            flexWrap: "wrap",
          }}
        >
          <div>
            <span className="eyebrow">
              MY TEAM
            </span>

            <h2
              style={{
                margin: "4px 0 0",
              }}
            >
              {teamLoading
                ? "Loading..."
                : myTeam?.team?.name ||
                  "No team yet"}
            </h2>
          </div>

          {!teamLoading && !myTeam?.team && (
            <button
              type="button"
              className="primary-btn"
              onClick={() =>
                setShowCreateTeam(
                  !showCreateTeam
                )
              }
            >
              <Users size={16} />

              {showCreateTeam
                ? "Cancel"
                : "Create Team"}
            </button>
          )}
        </div>

        {teamLoading ? (
          <p className="muted">
            Loading your team...
          </p>
        ) : myTeam?.team ? (
          <>
            <p className="muted">
              Your current team has{" "}
              <strong>
                {teamMemberCount}
              </strong>{" "}
              member
              {teamMemberCount !== 1
                ? "s"
                : ""}.
            </p>

            <div
              style={{
                display: "grid",
                gap: "10px",
                marginTop: "16px",
              }}
            >
              {myTeam.members.map(
                (member) => (
                  <div
                    key={member.student_id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "12px",
                      padding: "10px",
                      border:
                        "1px solid var(--border, #ddd)",
                      borderRadius: "10px",
                    }}
                  >
                    <Avatar
                      name={
                        member.name ||
                        "Student"
                      }
                      online
                    />

                    <div>
                      <strong>
                        {member.name}
                      </strong>

                      <p
                        className="muted"
                        style={{
                          margin: "2px 0 0",
                        }}
                      >
                        {
                          member.college_email
                        }
                      </p>
                    </div>
                  </div>
                )
              )}
            </div>
          </>
        ) : (
          <>
            <p className="muted">
              You are not part of a team yet.
              Create a team to start inviting
              classmates.
            </p>

            {showCreateTeam && (
              <div
                style={{
                  display: "flex",
                  gap: "10px",
                  marginTop: "16px",
                  flexWrap: "wrap",
                }}
              >
                <input
                  type="text"
                  placeholder="Enter team name..."
                  value={teamName}
                  onChange={(event) => {
                    setTeamName(
                      event.target.value
                    );
                    setError("");
                  }}
                  onKeyDown={(event) => {
                    if (
                      event.key === "Enter"
                    ) {
                      createTeam();
                    }
                  }}
                  style={{
                    flex: "1",
                    minWidth: "220px",
                  }}
                />

                <button
                  type="button"
                  className="primary-btn"
                  disabled={creatingTeam}
                  onClick={createTeam}
                >
                  <Users size={16} />

                  {creatingTeam
                    ? "Creating..."
                    : "Create Team"}
                </button>
              </div>
            )}
          </>
        )}
      </section>

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

      {/* Active Assignment */}
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
          <span>Team members</span>

          <strong>
            {teamMemberCount} / 4
          </strong>

          <small>
            {pendingInvitationCount} pending
            invitation
            {pendingInvitationCount !== 1
              ? "s"
              : ""}
          </small>
        </div>
      </section>

      {/* Search */}
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

      {/* Filters */}
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

      {/* Errors */}
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

      {/* Success */}
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

      {/* Candidates */}
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

              const isPending =
                sentInvitationIds.has(
                  Number(studentId)
                );

              const isSending =
                sendingId === studentId;

              const isCurrentUser =
                Number(studentId) ===
                Number(user?.id);

              const isTeamFull =
                teamMemberCount >= 4;

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
                      isCurrentUser ||
                      !myTeam?.team ||
                      isTeamFull
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
                    ) : !myTeam?.team ? (
                      <>
                        <Users size={16} />
                        Create Team First
                      </>
                    ) : isTeamFull ? (
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