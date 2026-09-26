import React, { useEffect, useState } from "react";
import { Hash, MoreHorizontal, Search, Send, Users } from "lucide-react";
import { useParams } from "react-router-dom";
import Avatar from "../components/Avatar";
import SectionHeader from "../components/SectionHeader";
import api from "../api/api";

const initialMessages = [
  {
    name: "Rahul",
    text: "Anyone doing the DBMS assignment?",
    time: "10:18",
  },
  {
    name: "Priya",
    text: "Yeah, I started with normalization. I'll share notes.",
    time: "10:20",
  },
  {
    name: "Aryan",
    text: "Thanks! That would help.",
    time: "10:21",
  },
];

export default function Room() {
  const { roomId } = useParams();

  const [room, setRoom] = useState(null);
  const [loading, setLoading] = useState(true);

  const [messages, setMessages] = useState(initialMessages);
  const [value, setValue] = useState("");

  useEffect(() => {
    if (!roomId) return;

    const loadRoom = async () => {
      try {
        setLoading(true);

        const response = await api.get(`/rooms/${roomId}`);

        setRoom(response.data);
      } catch (error) {
        console.error("Failed to load room:", error);
      } finally {
        setLoading(false);
      }
    };

    loadRoom();
  }, [roomId]);

  const send = () => {
    if (!value.trim()) return;

    setMessages([
      ...messages,
      {
        name: "You",
        text: value.trim(),
        time: "now",
      },
    ]);

    setValue("");
  };

  const roomName =
    room?.name ||
    room?.room_name ||
    room?.title ||
    "Academic Room";

  const roomDescription =
    room?.description ||
    "Your verified class community.";

  if (loading) {
    return <div>Loading room...</div>;
  }

  return (
    <>
      <SectionHeader
        eyebrow="ACADEMIC ROOM"
        title={roomName}
        description={roomDescription}
        action={
          <button className="secondary-btn">
            <Users size={17} />
            {room?.member_count || "Members"}
          </button>
        }
      />

      <div className="room-layout panel">
        <aside className="room-members">
          <div className="room-side-title">
            <strong>Members</strong>

            <button className="icon-btn">
              <Search size={16} />
            </button>
          </div>

          <div className="member-search">
            <Search size={15} />
            <input placeholder="Find a classmate" />
          </div>

          <div className="member-item">
            <Avatar name="Room members" online={false} />

            <div>
              <strong>Room loaded</strong>
              <span>
                Member list API not connected yet
              </span>
            </div>
          </div>
        </aside>

        <section className="chat">
          <div className="chat-header">
            <div>
              <Hash size={18} />
              <strong>general</strong>
            </div>

            <MoreHorizontal size={19} />
          </div>

          <div className="chat-messages">
            {messages.map((message, index) => (
              <div
                className={`message ${
                  message.name === "You" ? "mine" : ""
                }`}
                key={index}
              >
                <Avatar name={message.name} />

                <div>
                  <div className="message-meta">
                    <strong>{message.name}</strong>
                    <span>{message.time}</span>
                  </div>

                  <p>{message.text}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && send()
              }
              placeholder="Message Comps-A..."
            />

            <button
              className="primary-icon"
              onClick={send}
            >
              <Send size={17} />
            </button>
          </div>

          <p className="chat-note">
            Realtime messaging will be connected when the
            backend messaging/WebSocket API is available.
          </p>
        </section>
      </div>
    </>
  );
}