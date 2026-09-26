import React, { useEffect, useState } from "react";
import {
  CalendarDays,
  Clock3,
  MapPin,
  Plus,
  Search,
  X,
  Pencil,
} from "lucide-react";

import SectionHeader from "../components/SectionHeader";
import api from "../api/api";

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    event_type: "Workshop",
    start_time: "",
    end_time: "",
    location: "",
  });

  const loadEvents = async () => {
    try {
      setLoading(true);

      const response = await api.get("/events");

      setEvents(response.data || []);
    } catch (error) {
      console.error("Failed to load events:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setForm({
      title: "",
      description: "",
      event_type: "Workshop",
      start_time: "",
      end_time: "",
      location: "",
    });

    setEditingId(null);
    setShowForm(false);
  };

  const createEvent = async (e) => {
    e.preventDefault();

    try {
      setSaving(true);

      await api.post("/events", {
        title: form.title,
        description: form.description || null,
        event_type: form.event_type,
        start_time: new Date(form.start_time).toISOString(),
        end_time: new Date(form.end_time).toISOString(),
        location: form.location || null,
      });

      resetForm();
      await loadEvents();
    } catch (error) {
      console.error("Failed to create event:", error);

      alert(
        error.response?.data?.detail ||
          "Failed to create event."
      );
    } finally {
      setSaving(false);
    }
  };

  const editEvent = (event) => {
    setEditingId(event.id);

    setForm({
      title: event.title || "",
      description: event.description || "",
      event_type: event.event_type || "Workshop",
      start_time: event.start_time
        ? new Date(event.start_time).toISOString().slice(0, 16)
        : "",
      end_time: event.end_time
        ? new Date(event.end_time).toISOString().slice(0, 16)
        : "",
      location: event.location || "",
    });

    setShowForm(true);
  };

  const updateEvent = async (e) => {
    e.preventDefault();

    try {
      setSaving(true);

      await api.patch(`/events/${editingId}`, {
        title: form.title,
        description: form.description || null,
        event_type: form.event_type,
        start_time: new Date(form.start_time).toISOString(),
        end_time: new Date(form.end_time).toISOString(),
        location: form.location || null,
      });

      resetForm();
      await loadEvents();
    } catch (error) {
      console.error("Failed to update event:", error);

      alert(
        error.response?.data?.detail ||
          "Failed to update event."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleSubmit = async (e) => {
    if (editingId) {
      await updateEvent(e);
    } else {
      await createEvent(e);
    }
  };

  const deleteEvent = async (eventId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this event?"
    );

    if (!confirmed) return;

    try {
      setDeletingId(eventId);

      await api.delete(`/events/${eventId}`);

      await loadEvents();
    } catch (error) {
      console.error("Failed to delete event:", error);

      alert(
        error.response?.data?.detail ||
          "Failed to delete event."
      );
    } finally {
      setDeletingId(null);
    }
  };

  const filteredEvents = events.filter((event) =>
    event.title?.toLowerCase().includes(search.toLowerCase())
  );

  const formatDate = (dateString) => {
    if (!dateString) return "Date not available";

    return new Date(dateString).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const formatTime = (dateString) => {
    if (!dateString) return "Time not available";

    return new Date(dateString).toLocaleTimeString("en-IN", {
      hour: "numeric",
      minute: "2-digit",
    });
  };

  return (
    <>
      <SectionHeader
        eyebrow="COLLEGE CALENDAR"
        title="Events"
        description="Discover workshops, hackathons, meetups and academic activities."
        action={
          <button
            className="primary-btn"
            onClick={() => {
              setEditingId(null);
              setShowForm(true);
            }}
          >
            <Plus size={17} />
            Create event
          </button>
        }
      />

      {showForm && (
        <div className="panel event-form">
          <div className="event-form-header">
            <h3>
              {editingId ? "Edit Event" : "Create Event"}
            </h3>

            <button
              className="icon-btn"
              type="button"
              onClick={resetForm}
            >
              <X size={18} />
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="event-form-grid">
              <div className="event-form-group">
                <label htmlFor="event-title">
                  Event title
                </label>

                <input
                  id="event-title"
                  name="title"
                  placeholder="Event title"
                  value={form.title}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="event-form-group">
                <label htmlFor="event-type">
                  Event type
                </label>

                <select
                  id="event-type"
                  name="event_type"
                  value={form.event_type}
                  onChange={handleChange}
                >
                  <option value="Workshop">Workshop</option>
                  <option value="Hackathon">Hackathon</option>
                  <option value="Meetup">Meetup</option>
                  <option value="Academic">Academic</option>
                  <option value="Competition">
                    Competition
                  </option>
                </select>
              </div>

              <div className="event-form-group full-width">
                <label htmlFor="event-description">
                  Description
                </label>

                <textarea
                  id="event-description"
                  name="description"
                  placeholder="Describe the event..."
                  value={form.description}
                  onChange={handleChange}
                />
              </div>

              <div className="event-form-group">
                <label htmlFor="event-location">
                  Location
                </label>

                <input
                  id="event-location"
                  name="location"
                  placeholder="Location"
                  value={form.location}
                  onChange={handleChange}
                />
              </div>

              <div className="event-form-group">
                <label htmlFor="event-start">
                  Start time
                </label>

                <input
                  id="event-start"
                  type="datetime-local"
                  name="start_time"
                  value={form.start_time}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="event-form-group">
                <label htmlFor="event-end">
                  End time
                </label>

                <input
                  id="event-end"
                  type="datetime-local"
                  name="end_time"
                  value={form.end_time}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="event-form-actions">
                <button
                  className="icon-btn"
                  type="button"
                  onClick={resetForm}
                  disabled={saving}
                >
                  Cancel
                </button>

                <button
                  className="primary-btn"
                  type="submit"
                  disabled={saving}
                >
                  {saving
                    ? editingId
                      ? "Saving..."
                      : "Creating..."
                    : editingId
                    ? "Save Changes"
                    : "Create Event"}
                </button>
              </div>
            </div>
          </form>
        </div>
      )}

      <div className="toolbar panel">
        <div className="search-field">
          <Search size={17} />

          <input
            placeholder="Search events..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="panel">
          Loading events...
        </div>
      ) : filteredEvents.length === 0 ? (
        <div className="panel">
          No events found.
        </div>
      ) : (
        <div className="events-grid">
          {filteredEvents.map((event) => (
            <article
              className="event-card panel"
              key={event.id}
            >
              <div className="event-cover">
                <span>{event.event_type}</span>
                <CalendarDays size={30} />
              </div>

              <div className="event-card-body">
                <h3>{event.title}</h3>

                {event.description && (
                  <p className="muted">
                    {event.description}
                  </p>
                )}

                <div className="event-detail">
                  <CalendarDays size={15} />
                  {formatDate(event.start_time)}
                </div>

                <div className="event-detail">
                  <Clock3 size={15} />
                  {formatTime(event.start_time)}
                  {" - "}
                  {formatTime(event.end_time)}
                </div>

                <div className="event-detail">
                  <MapPin size={15} />
                  {event.location ||
                    "Location not available"}
                </div>

                <div className="event-card-footer">
                  <span
                    className={`event-status ${event.status}`}
                  >
                    {event.status}
                  </span>

                  <div className="event-actions">
                    <button
                      className="edit-event-btn"
                      onClick={() => editEvent(event)}
                      title="Edit event"
                    >
                      <Pencil size={13} />
                      Edit
                    </button>

                    <button
                      className="icon-btn"
                      onClick={() =>
                        deleteEvent(event.id)
                      }
                      disabled={
                        deletingId === event.id
                      }
                      title="Delete event"
                    >
                      {deletingId === event.id
                        ? "..."
                        : "Delete"}
                    </button>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </>
  );
}