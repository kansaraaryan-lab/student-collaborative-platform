import React, { useEffect, useState } from "react";
import {
  Edit3,
  GraduationCap,
  MapPin,
  Plus,
  ExternalLink,
} from "lucide-react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import SectionHeader from "../components/SectionHeader";
import Avatar from "../components/Avatar";
import api from "../api/api";

export default function Profile() {
  const { id } = useParams();
  const { user } = useAuth();

  const studentId = id || user?.id;
  const own = !id || String(id) === String(user?.id);

  const [student, setStudent] = useState(null);
  const [profile, setProfile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [availableSkills, setAvailableSkills] = useState([]);

  const [addingSkill, setAddingSkill] = useState(false);
  const [selectedSkill, setSelectedSkill] = useState("");
  const [proficiency, setProficiency] = useState("Beginner");

  const [loading, setLoading] = useState(true);

  // Edit profile state
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  const [form, setForm] = useState({
    bio: "",
    profile_picture: "",
    github_url: "",
    linkedin_url: "",
  });

  // Load student profile and skills
  useEffect(() => {
    if (!studentId) return;

    const loadProfile = async () => {
      try {
        setLoading(true);

        const [
          studentResponse,
          profileResponse,
          skillsResponse,
          allSkillsResponse,
        ] = await Promise.all([
          api.get(`/students/${studentId}`),

          api.get(`/students/${studentId}/profile`).catch((error) => {
            if (error.response?.status === 404) {
              return { data: null };
            }

            throw error;
          }),

          api.get(`/students/${studentId}/skills`).catch((error) => {
            if (error.response?.status === 404) {
              return { data: [] };
            }

            throw error;
          }),

          api.get(`/skills`),
        ]);

        setStudent(studentResponse.data);
        setProfile(profileResponse.data);

        // Store all available skills
        setAvailableSkills(allSkillsResponse.data || []);

        // Create skill lookup map
        const skillMap = Object.fromEntries(
          allSkillsResponse.data.map((skill) => [skill.id, skill])
        );

        // Combine student skill relationship with skill details
        const studentSkills = (skillsResponse.data || []).map(
          (studentSkill) => ({
            ...studentSkill,
            skill: skillMap[studentSkill.skill_id],
          })
        );

        setSkills(studentSkills);

        if (profileResponse.data) {
          setForm({
            bio: profileResponse.data.bio || "",
            profile_picture:
              profileResponse.data.profile_picture || "",
            github_url: profileResponse.data.github_url || "",
            linkedin_url:
              profileResponse.data.linkedin_url || "",
          });
        }
      } catch (error) {
        console.error("Failed to load profile:", error);
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [studentId]);

  // Handle profile form changes
  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  // Save profile
  const saveProfile = async () => {
    if (!studentId) return;

    try {
      setSaving(true);

      const response = await api.patch(
        `/students/${studentId}/profile`,
        form
      );

      setProfile(response.data);

      setForm({
        bio: response.data.bio || "",
        profile_picture:
          response.data.profile_picture || "",
        github_url: response.data.github_url || "",
        linkedin_url:
          response.data.linkedin_url || "",
      });

      setEditing(false);
    } catch (error) {
      console.error("Failed to update profile:", error);
    } finally {
      setSaving(false);
    }
  };

  // Cancel profile editing
  const cancelEdit = () => {
    setForm({
      bio: profile?.bio || "",
      profile_picture:
        profile?.profile_picture || "",
      github_url: profile?.github_url || "",
      linkedin_url:
        profile?.linkedin_url || "",
    });

    setEditing(false);
  };

  // Add technical skill
  const addSkill = async () => {
    if (!studentId || !selectedSkill) return;

    try {
      const response = await api.post("/student-skills", {
        student_id: Number(studentId),
        skill_id: Number(selectedSkill),
        proficiency,
      });

      console.log("Skill added:", response.data);

      // Reload student's skills
      const skillsResponse = await api.get(
        `/students/${studentId}/skills`
      );

      // Recreate skill lookup map
      const skillMap = Object.fromEntries(
        availableSkills.map((skill) => [skill.id, skill])
      );

      // Combine relationship data with skill details
      const studentSkills = (skillsResponse.data || []).map(
        (studentSkill) => ({
          ...studentSkill,
          skill: skillMap[studentSkill.skill_id],
        })
      );

      setSkills(studentSkills);

      // Reset skill form
      setSelectedSkill("");
      setProficiency("Beginner");
      setAddingSkill(false);
    } catch (error) {
      console.error("Failed to add skill:", error);

      if (error.response?.status === 409) {
        alert("You already have this skill.");
      } else {
        alert("Failed to add skill.");
      }
    }
  };
// Remove a skill 

const removeSkill = async (skillId) => {
  if (!studentId || !skillId) return;

  try {
    await api.delete(
      `/students/${studentId}/skills/${skillId}`
    );

    // Reload student's skills
    const skillsResponse = await api.get(
      `/students/${studentId}/skills`
    );

    const skillMap = Object.fromEntries(
      availableSkills.map((skill) => [skill.id, skill])
    );

    const studentSkills = (skillsResponse.data || []).map(
      (studentSkill) => ({
        ...studentSkill,
        skill: skillMap[studentSkill.skill_id],
      })
    );

    setSkills(studentSkills);
  } catch (error) {
    console.error("Failed to remove skill:", error);
    alert("Failed to remove skill.");
  }
};

  if (loading) {
    return <div>Loading profile...</div>;
  }

  const studentName =
    student?.name ||
    student?.full_name ||
    user?.name ||
    "Student";

  const studentEmail =
    student?.email ||
    student?.college_email ||
    user?.email ||
    "";

  const studentYear = profile?.year || "Not available";

const studentBranch = profile?.branch || "Not available";

const studentRoom = student?.room_id
  ? `Room ${student.room_id}`
  : "No room assigned";

  const technicalSkills = skills
  .filter((item) => item.skill)
  .map((item) => ({
    id: item.skill_id,
    name:
      item.skill.name ||
      item.skill.skill_name,
  }))
  .filter((item) => item.name);

  return (
    <>
      <SectionHeader
        eyebrow="PROFILE"
        title={own ? "My profile" : "Student profile"}
        description="Your academic identity and collaboration profile."
        action={
          own &&
          !editing && (
            <button
              className="secondary-btn"
              onClick={() => setEditing(true)}
            >
              <Edit3 size={17} />
              Edit profile
            </button>
          )
        }
      />

      <div className="profile-layout">
        {/* Profile summary */}
        <aside className="profile-summary panel">
          <Avatar
            name={studentName}
            size="large"
            online
          />

          <h2>{studentName}</h2>

          <p className="muted">
            {studentEmail}
          </p>

          <div className="profile-meta">
            <GraduationCap size={16} />
            {studentYear} · {studentBranch}
          </div>

          <div className="profile-meta">
            <MapPin size={16} />
            {studentRoom}
          </div>

          <div className="profile-actions">
            <button className="primary-btn full">
              Message
            </button>

            <button className="secondary-btn full">
              View projects
            </button>
          </div>
        </aside>

        <div className="profile-content">
          {/* Edit Profile */}
          {editing ? (
            <section className="panel">
              <div className="panel-header">
                <h3>Edit Profile</h3>
              </div>

              <div className="profile-form">
                <label>
                  Bio

                  <textarea
                    name="bio"
                    value={form.bio}
                    onChange={handleChange}
                    placeholder="Tell others about yourself..."
                    rows={5}
                  />
                </label>

                <label>
                  GitHub URL

                  <input
                    type="url"
                    name="github_url"
                    value={form.github_url}
                    onChange={handleChange}
                    placeholder="https://github.com/username"
                  />
                </label>

                <label>
                  LinkedIn URL

                  <input
                    type="url"
                    name="linkedin_url"
                    value={form.linkedin_url}
                    onChange={handleChange}
                    placeholder="https://linkedin.com/in/username"
                  />
                </label>

                <div className="profile-form-actions">
                  <button
                    className="secondary-btn"
                    onClick={cancelEdit}
                    disabled={saving}
                  >
                    Cancel
                  </button>

                  <button
                    className="primary-btn"
                    onClick={saveProfile}
                    disabled={saving}
                  >
                    {saving
                      ? "Saving..."
                      : "Save changes"}
                  </button>
                </div>
              </div>
            </section>
          ) : (
            <>
              {/* About */}
              <section className="panel">
                <div className="panel-header">
                  <h3>About</h3>

                  {own && (
                    <Edit3
                      size={16}
                      onClick={() =>
                        setEditing(true)
                      }
                      style={{
                        cursor: "pointer",
                      }}
                    />
                  )}
                </div>

                <p className="about-text">
                  {profile?.bio ||
                    "No bio added yet."}
                </p>
              </section>

              {/* Technical Skills */}
              <section className="panel">
                <div className="panel-header">
                  <h3>Technical skills</h3>

                  {own && (
                    <button
                      className="icon-btn"
                      onClick={() =>
                        setAddingSkill(
                          !addingSkill
                        )
                      }
                    >
                      <Plus size={17} />
                    </button>
                  )}
                </div>

                {/* Add Skill Form */}
                {addingSkill && (
                  <div className="profile-form">
                    <label>
                      Skill

                      <select
                        value={selectedSkill}
                        onChange={(event) =>
                          setSelectedSkill(
                            event.target.value
                          )
                        }
                      >
                        <option value="">
                          Select a skill
                        </option>

                        {availableSkills.map(
                          (skill) => (
                            <option
                              key={skill.id}
                              value={skill.id}
                            >
                              {skill.name}
                            </option>
                          )
                        )}
                      </select>
                    </label>

                    <label>
                      Proficiency

                      <select
                        value={proficiency}
                        onChange={(event) =>
                          setProficiency(
                            event.target.value
                          )
                        }
                      >
                        <option value="Beginner">
                          Beginner
                        </option>

                        <option value="Intermediate">
                          Intermediate
                        </option>

                        <option value="Advanced">
                          Advanced
                        </option>
                      </select>
                    </label>

                    <div className="profile-form-actions">
                      <button
                        className="secondary-btn"
                        onClick={() => {
                          setAddingSkill(false);
                          setSelectedSkill("");
                          setProficiency(
                            "Beginner"
                          );
                        }}
                      >
                        Cancel
                      </button>

                      <button
                        className="primary-btn"
                        disabled={!selectedSkill}
                        onClick={addSkill}
                      >
                        Add skill
                      </button>
                    </div>
                  </div>
                )}

                {/* Existing Skills */}
                <div className="tag-list">
               {technicalSkills.length > 0 ? (
  technicalSkills.map((skill) => (
    <span
      className="tag skill-tag"
      key={skill.id}
    >
      {skill.name}

      {own && (
        <button
          type="button"
          className="skill-remove-btn"
          onClick={() => removeSkill(skill.id)}
          aria-label={`Remove ${skill.name}`}
        >
          ×
        </button>
      )}
    </span>
  ))
) : (
  <span className="muted">
    No skills added yet.
  </span>
)}
                </div>
              </section>

             

              {/* Projects */}
              <section className="panel">
                <div className="panel-header">
                  <h3>Projects</h3>

                  {own && (
                    <button className="icon-btn">
                      <Plus size={17} />
                    </button>
                  )}
                </div>

                <div className="project-list">
                  {/* GitHub */}
                  <div className="project-card">
                    <div className="project-icon">
                      <ExternalLink
                        size={18}
                      />
                    </div>

                    <div>
                      <strong>
                        GitHub Projects
                      </strong>

                      <span>
                        View student's GitHub
                        profile
                      </span>

                      <small>
                        {profile?.github_url ||
                          "GitHub not added"}
                      </small>
                    </div>

                    {profile?.github_url && (
                      <ExternalLink
                        size={16}
                        className="row-arrow"
                        onClick={() =>
                          window.open(
                            profile.github_url,
                            "_blank"
                          )
                        }
                      />
                    )}
                  </div>

                  {/* LinkedIn */}
                  <div className="project-card">
                    <div className="project-icon">
                      <ExternalLink
                        size={18}
                      />
                    </div>

                    <div>
                      <strong>
                        LinkedIn
                      </strong>

                      <span>
                        Student professional
                        profile
                      </span>

                      <small>
                        {profile?.linkedin_url ||
                          "LinkedIn not added"}
                      </small>
                    </div>

                    {profile?.linkedin_url && (
                      <ExternalLink
                        size={16}
                        className="row-arrow"
                        onClick={() =>
                          window.open(
                            profile.linkedin_url,
                            "_blank"
                          )
                        }
                      />
                    )}
                  </div>
                </div>
              </section>
            </>
          )}
        </div>
      </div>
    </>
  );
}