import React, { useState } from "react";

export default function AskBox({ onSubmit }) {
  const [q, setQ] = useState("");
  return (
    <div>
      <textarea value={q} onChange={(e)=>setQ(e.target.value)} rows={4} style={{ width: "100%" }} placeholder="Type a math question (e.g., integrate x^2 dx)"/>
      <button onClick={()=> { if(q.trim()) onSubmit(q.trim()); }} style={{ marginTop: 8 }}>Ask</button>
    </div>
  );
}
