import React from "react";
import { Flame, Pause, Play, Users, Trophy, TreePine } from "lucide-react";
import { useState } from "react";
import SectionHeader from "../components/SectionHeader";

export default function StudyRoom() {
  const [running, setRunning] = useState(true);

  return (
    <>
      <SectionHeader eyebrow="FOCUS TOGETHER" title="Study Room" description="Build study habits with your classmates." action={<button className="secondary-btn"><Users size={17} /> 4 participants</button>} />

      <div className="study-grid">
        <section className="study-main panel">
          <div className="study-status"><span className="live-dot" /> SESSION IN PROGRESS</div>
          <div className="timer">01:42:31</div>
          <p className="muted">Deep work session · started 10:15 AM</p>

          <div className="study-tree">
            <div className="tree-stars">✦ ✦ ✦</div>
            <TreePine size={132} strokeWidth={1.1} />
            <div className="tree-ground" />
          </div>

          <div className="study-controls">
            <button className="secondary-btn" onClick={() => setRunning(!running)}>
              {running ? <><Pause size={17} /> Pause</> : <><Play size={17} /> Resume</>}
            </button>
            <button className="danger-btn">End session</button>
          </div>
          <p className="security-note">Study duration will be verified server-side when the backend is connected.</p>
        </section>

        <aside className="study-side">
          <section className="panel">
            <div className="panel-header"><h3>Participants</h3><Users size={17} /></div>
            {["Sanskruti", "Aryan", "Priya", "Rahul"].map((name) => <div className="participant" key={name}><span className="status-dot" /><strong>{name}</strong><small>Studying</small></div>)}
          </section>

          <section className="panel">
            <div className="panel-header"><h3>Weekly leaderboard</h3><Trophy size={17} /></div>
            <div className="leader"><b>01</b><span>Group A</span><strong>18h 32m</strong></div>
            <div className="leader"><b>02</b><span>Group B</span><strong>16h 10m</strong></div>
            <div className="leader"><b>03</b><span>Group C</span><strong>14h 45m</strong></div>
          </section>

          <section className="streak-card">
            <Flame size={25} />
            <div><span>Current streak</span><strong>5 days 🔥</strong></div>
          </section>
        </aside>
      </div>
    </>
  );
}