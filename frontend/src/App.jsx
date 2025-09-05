import React, { useState } from "react";
import AskBox from "./components/AskBox";
import AnswerCard from "./components/AnswerCard";
import Feedback from "./components/Feedback";

export default function App() {
  const [answer, setAnswer] = useState(null);
  const [question, setQuestion] = useState("");

  return (
    <div style={{ padding: 20, fontFamily: "Inter, sans-serif", maxWidth: 900, margin: "0 auto" }}>
      <h1>Math Agent (Agentic RAG)</h1>
      <AskBox onSubmit={async (q) => {
        setQuestion(q);
        setAnswer({loading: true});
        const res = await fetch("/api/ask", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ question: q, allow_web: true })
        });
        const data = await res.json();
        setAnswer({loading: false, data})
      }} />
      {answer && !answer.loading && answer.data && (
        <div style={{ marginTop: 20 }}>
          <AnswerCard question={question} result={answer.data} />
          <Feedback question={question} answer={answer.data.answer} />
        </div>
      )}
    </div>
  );
}
