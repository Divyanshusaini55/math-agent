import React from "react";

export default function AnswerCard({ question, result }) {
  if (!result) return null;
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <b>Question:</b>
      <div>{question}</div>
      <hr/>
      <b>Answer:</b>
      <pre style={{ whiteSpace: "pre-wrap" }}>{result.answer || result.error}</pre>
      {!result.ok && result.validation_reason && <div style={{ color: "orange" }}>Validation warning: {result.validation_reason}</div>}
      {result.used_kb && <div style={{ marginTop: 8, fontSize: 12, color: "#555" }}>Used KB</div>}
    </div>
  );
}
