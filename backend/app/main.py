# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid
import asyncio
import sqlite3
import os
from agent import answer_question
from vectorstore import upsert

app = FastAPI(title="Math Agent API")

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
    id TEXT PRIMARY KEY,
    question TEXT,
    answer TEXT,
    rating INTEGER,
    comment TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)""")
conn.commit()
conn.close()

class AskReq(BaseModel):
    question: str
    allow_web: Optional[bool] = True

class FeedbackReq(BaseModel):
    question: str
    answer: str
    rating: int
    comment: Optional[str] = None
    add_to_kb: Optional[bool] = False

@app.post("/ask")
async def ask(req: AskReq):
    out = await answer_question(req.question, allow_web=req.allow_web)
    return out
# NEW: Support frontend calling /api/ask
@app.post("/api/ask")
async def api_ask(req: AskReq):
    return await ask(req)


@app.post("/feedback")
def feedback(req: FeedbackReq):
    id_ = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO feedback (id, question, answer, rating, comment) VALUES (?,?,?,?,?)",
                 (id_, req.question, req.answer, req.rating, req.comment))
    conn.commit()
    conn.close()
    if req.add_to_kb:
        async def _u():
            await upsert(str(uuid.uuid4()), req.question + "\nAnswer: " + req.answer, {"source": "user_feedback"})
        asyncio.create_task(_u())
    return {"ok": True}
