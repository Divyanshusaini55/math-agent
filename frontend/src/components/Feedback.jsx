import React, { useState } from "react";

export default function Feedback({ question, answer }) {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [added, setAdded] = useState(false);

  const submit = async (addToKb=false) => {
    await fetch("/api/feedback", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ question, answer, rating, comment, add_to_kb: addToKb })
    });
    setAdded(true);
  };

  if (added) return <div>Thanks for the feedback!</div>;

  return (
    <div style={{ marginTop: 12 }}>
      <b>Feedback</b>
      <div>
        <label>Rating: </label>
        <select value={rating} onChange={(e)=>setRating(Number(e.target.value))}>
          <option value={5}>5 - Excellent</option>
          <option value={4}>4 - Good</option>
          <option value={3}>3 - Okay</option>
          <option value={2}>2 - Poor</option>
          <option value={1}>1 - Bad</option>
        </select>
      </div>
      <div>
        <textarea value={comment} onChange={(e)=>setComment(e.target.value)} placeholder="Optional comment" rows={2} style={{ width: "100%" }} />
      </div>
      <div style={{ marginTop: 8 }}>
        <button onClick={()=>submit(false)}>Submit Feedback</button>
        <button style={{ marginLeft: 8 }} onClick={()=>submit(true)}>Submit & Add to KB</button>
      </div>
    </div>
  );
}
