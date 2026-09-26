import React, { useEffect, useState } from "react";
import { Search,  Users } from "lucide-react";
import { useParams,useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Avatar from "../components/Avatar";
import SectionHeader from "../components/SectionHeader";
import api from "../api/api";


export default function Room() {
  
const { roomId } = useParams();
const {user} = useAuth();
const navigate = useNavigate();
const [room, setRoom] = useState(null);
const [members, setMembers] = useState([]);
const [loading, setLoading] = useState(true);
const [search , setSearch] = useState("");
const actualRoomId = user?.roomId;
 
  useEffect(() => {
    if (!actualRoomId) return;
    const loadRoom = async () => {
      try {
        setLoading(true);

     const response = await api.get(`/rooms/${actualRoomId}`);
        setRoom(response.data);

        const studentsResponse = await api.get("/students");

const roomMembers = studentsResponse.data.filter(
  (student) => student.room_id === Number(actualRoomId)
);

setMembers(roomMembers);
      } catch (error) {
        console.error("Failed to load room:", error);
      } finally {
        setLoading(false);
      }
    };

    loadRoom();
}, [actualRoomId]);



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
           {members.length} Members
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
            <input
           placeholder="Find a classmate"
           value={search}
           onChange={(e) => setSearch(e.target.value)}
/>
          </div>

     {members.length === 0 ? (
  <p className="muted">No students found in this class.</p>
) : members.filter((member) =>
    member.name.toLowerCase().includes(search.toLowerCase())
  ).length === 0 ? (
  <p className="muted">No classmates match your search.</p>
) : (


  members
  .filter((member) =>
    member.name.toLowerCase().includes(search.toLowerCase())
  )
  .map((member) => (
   <div
  className="member-item"
  key={member.id}
  onClick={() => navigate(`/profile/${member.id}`)}
  style={{ cursor: "pointer" }}
>
      <Avatar name={member.name} online={false} />

      <div>
        <strong>{member.name}</strong>
        <span>{member.college_email}</span>
      </div>
    </div>
  ))
)}
        </aside>

       
      </div>
    </>
  );
}