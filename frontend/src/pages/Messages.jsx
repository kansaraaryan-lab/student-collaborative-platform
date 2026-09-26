import  { useRef, useEffect, useState } from "react";
import {
  MoreHorizontal,
  Paperclip,
  Search,
  Send,
  Smile,
} from "lucide-react";
import EmojiPicker from "emoji-picker-react";

import Avatar from "../components/Avatar";
import SectionHeader from "../components/SectionHeader";
import api from "../api/api";
import { useAuth } from "../context/useAuth";

export default function Messages() {
  const { user } = useAuth();
  const socketRef = useRef(null);

  const [value, setValue] = useState("");
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);

  // Fetch students from FastAPI
  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await api.get("/students");

        const otherStudents = response.data.filter(
          (student) => student.id !== user?.id
        );

        setStudents(otherStudents);

        if (otherStudents.length > 0) {
          setSelectedStudent(otherStudents[0]);
        }
      } catch (err) {
        console.error("Failed to load students:", err);
      }
    };

    if (user?.id) {
      fetchStudents();
    }
  }, [user?.id]);

  // Fetch message history from FastAPI
  useEffect(() => {
    const fetchMessages = async () => {
      if (!user?.id) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        const response = await api.get(`/messages/${user.id}`);

        setMessages(
          response.data.map((message) => ({
            ...message,
            mine: Number(message.sender_id) === Number(user.id),
            text: message.content,
            time: new Date(message.created_at).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            }),
          }))
        );
      } catch (err) {
        console.error("Failed to load messages:", err);
        setError("Failed to load messages.");
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, [user?.id]);

  // Connect to FastAPI WebSocket
  useEffect(() => {
    if (!user?.id) return;

    const socket = new WebSocket(
      `ws://127.0.0.1:8000/api/v1/ws/messages/${user.id}`
    );

    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          ...message,
          id: `ws-${Date.now()}-${Math.random()}`,
          mine: Number(message.sender_id) === Number(user.id),
          text: message.content,
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [user?.id]);

  // Filter messages for the selected student
  const filteredMessages = messages.filter((message) => {
    if (!selectedStudent?.id || !user?.id) {
      return false;
    }

    return (
      (Number(message.sender_id) === Number(user.id) &&
        Number(message.receiver_id) === Number(selectedStudent.id)) ||
      (Number(message.sender_id) === Number(selectedStudent.id) &&
        Number(message.receiver_id) === Number(user.id))
    );
  });

  // Get sender name
  const getSenderName = (message) => {
    // If current user sent the message
    if (Number(message.sender_id) === Number(user.id)) {
      return user.name || "You";
    }

    // Find sender in students list
    const sender = students.find(
      (student) => Number(student.id) === Number(message.sender_id)
    );

    return sender?.name || "Unknown Student";
  };

  // Send message through WebSocket
  const send = () => {
    const text = value.trim();

    if (!text) return;

    if (!selectedStudent?.id) {
      console.error("Please select a student");
      return;
    }

    if (
      !socketRef.current ||
      socketRef.current.readyState !== WebSocket.OPEN
    ) {
      console.error("WebSocket is not connected");
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        receiver_id: selectedStudent.id,
        content: text,
      })
    );

    setValue("");
  };

  return (
    <>
      <SectionHeader
        eyebrow="COMMUNICATION"
        title="Messages"
        description="Connect directly with your classmates."
      />

      <div className="messages-layout panel">
        {/* LEFT SIDE - STUDENT LIST */}
        <aside className="conversation-list">
          <div className="conversation-search">
            <Search size={16} />
            <input placeholder="Search messages" />
          </div>

          {students.map((student) => (
            <div
              className={`conversation ${
                selectedStudent?.id === student.id ? "active" : ""
              }`}
              key={student.id}
              onClick={() => setSelectedStudent(student)}
            >
              <Avatar name={student.name} online />

              <div>
                <strong>{student.name}</strong>
                <span>{student.college_email}</span>
              </div>
            </div>
          ))}
        </aside>

        {/* RIGHT SIDE - CHAT */}
        <section className="dm-chat">
          <header className="dm-header">
            <Avatar
              name={selectedStudent?.name || "Select a student"}
              online
            />

            <div>
              <strong>
                {selectedStudent?.name || "Select a student"}
              </strong>

              <span>
                {selectedStudent?.college_email ||
                  "Choose a student to start chatting"}
              </span>
            </div>

            <MoreHorizontal size={19} />
          </header>

          {/* MESSAGES */}
          <div className="dm-messages">
            {loading && <p>Loading messages...</p>}

            {!loading && error && <p>{error}</p>}

            {!loading &&
              !error &&
              filteredMessages.length === 0 && (
                <p>No messages yet.</p>
              )}

            {!loading &&
              !error &&
              filteredMessages.map((message) => (
                <div
                  className={`bubble ${message.mine ? "mine" : ""}`}
                  key={message.id}
                >
                  {/* SENDER NAME */}
                  <small className="message-sender">
                    {getSenderName(message)}
                  </small>

                  {/* MESSAGE */}
                  <p>{message.text}</p>

                  {/* TIME */}
                  <small>{message.time}</small>
                </div>
              ))}
          </div>

          {/* MESSAGE INPUT */}
         {showEmojiPicker && (
  <div className="emoji-picker">
    <EmojiPicker
      onEmojiClick={(emojiObject) => {
        setValue((current) => current + emojiObject.emoji);
        setShowEmojiPicker(false);
      }}
    />
  </div>
)}

<div className="dm-input">
            <button className="icon-btn">
              <Paperclip size={18} />
            </button>

            <input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Write a message..."
            />

            <button
  className="icon-btn"
  onClick={() => setShowEmojiPicker((current) => !current)}
>
  <Smile size={18} />
</button>

            <button className="primary-icon" onClick={send}>
              <Send size={17} />
            </button>
          </div>

          <p className="chat-note">
            Logged in as {user?.name || "Student"}
          </p>
        </section>
      </div>
    </>
  );
}