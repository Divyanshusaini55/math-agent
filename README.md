#  Math Agent Project

##  Overview
The **Math Agent** is an Agentic-RAG (Retrieval-Augmented Generation) system designed to behave like a mathematics professor.  

- Accepts **math questions** as input.  
- First checks a **knowledge base (Qdrant VectorDB)** for similar solved problems.  
- If found → generates a **step-by-step explanation** using **Gemini Pro**.  
- If not found → performs a **web search** (via MCP integration) and generates an answer.  
- Includes **guardrails** (input/output validation) and a **human-in-the-loop feedback mechanism** to improve over time.  
- Frontend built in **React (Vite)**, backend in **FastAPI**, vector database with **Qdrant**.

---

## Architecture
## 🏗️ Architecture (ASCII Diagram)

             ┌─────────────────────────────┐
             │         Frontend            │
             │       (React + Vite)        │
             └───────────────┬─────────────┘
                             │
                             ▼
             ┌─────────────────────────────┐
             │         Backend             │
             │      (FastAPI API)          │
             └───────────────┬─────────────┘
                             │
                   ┌─────────┴─────────┐
                   │   Agent Pipeline  │
                   └─────────┬─────────┘
                             │
      ┌────────────────────────────────────────────────┐
      │  Guardrails (input validation & SymPy check)   │
      └────────────────────────────────────────────────┘

      ┌────────────────────────────────────────────────┐
      │ Human-in-the-loop feedback (SQLite + KB update)│
      └────────────────────────────────────────────────┘




### System Diagram

### Workflow
1. **User enters a math question** on the frontend.  
2. **FastAPI backend** receives the request.  
3. **Guardrails** validate the input (must be a math question).  
4. **Vectorstore (Qdrant)** checks knowledge base.  
   - If match found → return KB-based explanation.  
   - If no match → call **Web Search (MCP)** and use Gemini Pro for reasoning.  
5. **Output Guardrails** validate result using **SymPy**.  
6. **Response returned** to the frontend.  
7. **User Feedback** stored in SQLite; optional corrections update KB.  

---

## ⚙ Components

### 1. **Backend (FastAPI)**
- **APIs**
  - `POST /ask` → Accept math question, return solution.  
  - `POST /feedback` → Store user feedback in SQLite, optionally update KB.  
  - `POST /admin/ingest` → Manually add Q/A pairs to KB.  

- **Modules**
  - `agent.py` → Core logic for routing between KB, Gemini, Web.  
  - `vectorstore.py` → Qdrant + Gemini embeddings for retrieval.  
  - `guardrails.py` → Input validation + output validation via SymPy.  
  - `searcher.py` → Web search fallback (Serper/Tavily).  
  - `ingest.py` → Seeding KB with examples.  
  - `main.py` → FastAPI entrypoint.  

---

### 2. **Frontend (React + Vite)**
- Components:
  - `AskBox` → Input for math questions.  
  - `AnswerCard` → Displays answer (with step-by-step explanation).  
  - `Feedback` → Collects user feedback & ratings.  

- Features:
  - Minimal UI (`styles.css`).  
  - API proxy setup in `vite.config.mjs`.  
  - Hot reload for dev.  

---

### 3. **Knowledge Base**
- Uses **Qdrant** for vector similarity search.  
- Embeddings generated via Gemini.  
- Example stored Q/As:  
  - `∫ x² dx = x³/3 + C`  
  - `Solve x² - 5x + 6 = 0 → roots 2, 3`

---

### 4. **Guardrails**
- **Input Guardrail** → Rejects non-math queries.  
- **Output Guardrail** → Uses **SymPy** to check expressions for correctness.  

---

### 5. **Feedback**
- Stored in `feedback.db` (SQLite).  
- Users rate answers (1–5) and optionally submit corrected solutions.  
- With `add_to_kb: true`, corrected answers update the knowledge base.  

---

##  Setup & Running

### 1. Clone Project
```bash
git clone <repo_url>
cd math-agent-project
