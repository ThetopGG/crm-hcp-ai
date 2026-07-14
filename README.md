# CRM HCP AI — AI-First CRM Module for Pharmaceutical Field Representatives

An AI-first CRM module that lets pharma field reps log doctor interactions in **plain natural language**. A real **LangGraph** agent detects intent, extracts structured data with an LLM (via **Groq**), writes to **PostgreSQL**, and auto-fills a structured form the rep can review and save.


# 1. Architecture Overview


┌─────────────────────┐        HTTPS/JSON        ┌──────────────────────────┐
│   React Frontend     │ ───────────────────────► │   FastAPI Backend         │
│  Redux Toolkit + MUI  │ ◄─────────────────────── │  SQLAlchemy + Pydantic    │
└─────────────────────┘                           └────────────┬─────────────┘
                                                                │
                                                     ┌──────────▼─────────────┐
                                                     │   LangGraph Agent       │
                                                     │  (intent → decision →   │
                                                     │   tool → llm → db →     │
                                                     │   response)             │
                                                     └──────────┬─────────────┘
                                                                │
                                                     ┌──────────▼─────────────┐
                                                     │  Groq LLM (llama-3.3-70b-versatile)│
                                                     └─────────────────────────┘
                                                                │
                                                     ┌──────────▼─────────────┐
                                                     │      PostgreSQL         │
                                                     └─────────────────────────┘

# Features

- AI-powered CRM for pharmaceutical field representatives
- LangGraph workflow with intent detection and tool routing
- 5 AI tools:
  - Log Interaction
  - Edit Interaction
  - Search Interaction
  - Follow-up Generation
  - Insights Generation
- Groq LLM integration
- PostgreSQL database
- JWT Authentication
- Material UI responsive frontend

# Tech Stack

**Frontend:** React 18, Redux Toolkit, React Router 6, Material UI 6, Axios, Google Inter Font (via `@fontsource/inter`), Vite.

**Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, LangGraph, LangChain, Groq API (via `langchain-groq`).

**Database:** PostgreSQL.







#  LangGraph Agent Explained

The agent implements exactly the flow required by the assignment:

```
User Input → Intent Detection → Decision Node → Tool Node → LLM → Database → Response
```

- **Intent Detection** (`nodes.intent_detection_node`) — calls the LLM to classify the rep's message into one of: `log_interaction`, `edit_interaction`, `search_interaction`, `follow_up`, `insights`, `general`.
- **Decision Node** (`nodes.decision_node`) — maps the intent to a concrete tool, falling back sensibly (e.g. an "edit" without a target interaction becomes a new "log").
- **Tool Node** (`nodes.tool_node`) — dispatches to one of the **five real LangGraph tools**:
  1. `log_interaction_tool` — summarizes, extracts entities, converts to structured JSON, and saves a new HCP + Interaction to Postgres.
  2. `edit_interaction_tool` — modifies an existing interaction from a natural-language instruction.
  3. `search_interaction_tool` — extracts filters (doctor/date/product/keyword) and searches the DB.
  4. `followup_tool` — generates a next-meeting agenda, an email draft, and a summary; saves a `FollowUp` record.
  5. `insights_tool` — aggregates CRM stats (interaction frequency, pending follow-ups, top products, doctor engagement) and asks the LLM to narrate them.
- **LLM Node** (`nodes.llm_response_node`) — turns the tool's raw result into a short, friendly confirmation message for the rep.
- **Database Node** (`nodes.database_node`) — confirms whether a record was actually persisted.
- **Response Node** (`nodes.response_node`) — assembles the final JSON payload returned to the frontend (reply, intent, extracted form, tool used, raw data).

The graph is built and compiled per-request in `app/langgraph_agent/graph.py` using `langgraph.graph.StateGraph`, with the DB session and current user bound into node closures via `functools.partial`.

### Switching Models

Every node/tool calls `app.services.llm_service.get_llm()`, which reads `settings.GROQ_MODEL`. **To switch from `gemma2-9b-it` to `llama-3.3-70b-versatile`, change exactly one line** — the `GROQ_MODEL` value in your `.env` file (or `app/config.py` default). No other code changes are required anywhere in the app.

---

# Database Schema

| Table          | Key Fields                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `users`        | id, full_name, email, hashed_password, role, is_active                     |
| `hcps`         | id, name, speciality, hospital, phone, email, city                         |
| `products`     | id, name, description, category                                            |
| `interactions` | id, hcp_id (FK), created_by (FK→users), interaction_date, interaction_type, products_discussed, notes, outcome, follow_up_date, raw_conversation, ai_summary |
| `follow_ups`   | id, interaction_id (FK), due_date, agenda, email_draft, summary, is_completed |

Tables are auto-created on backend startup via `Base.metadata.create_all()`. For production, use Alembic migrations instead.

---

# Setup & Installation

# Prerequisites

- Python 3.11+ (Tested on Python 3.13)
- Node.js 18+
- PostgreSQL 14+
- A free Groq API key: https://console.groq.com/keys

#  PostgreSQL Setup

```bash
# Using psql
createdb crm_hcp_ai

# or inside psql
psql -U postgres
CREATE DATABASE crm_hcp_ai;
```

# Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set:
#   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/crm_hcp_ai
#   GROQ_API_KEY=<your key from console.groq.com>
#   SECRET_KEY=<any long random string>

uvicorn app.main:app --reload --port 8000
```

Backend now running at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

### 5.3 Groq API Key Setup

1. Go to https://console.groq.com/keys
2. Create an API key.
3. Paste it into `backend/.env` as `GROQ_API_KEY`.
4. Default model is `gemma2-9b-it`. To use `llama-3.3-70b-versatile`, change `GROQ_MODEL` in `.env`.

### 5.4 Frontend Setup

```bash
cd frontend
npm install

cp .env.example .env
# Ensure VITE_API_BASE_URL=http://localhost:8000

npm run dev
```

Frontend now running at `http://localhost:5173`.

##  First Run

1. Open `http://localhost:5173`.
2. Click **Register**, create an account.
3. You'll be logged in automatically and redirected to the Dashboard.
4. Go to **Log Interaction** and try the AI Assistant, e.g.:
   > "I met Dr Sharma today at Apollo Hospital. We discussed CardX. He wants efficacy data next Monday."
5. Watch the structured form auto-fill on the left. Review and click **Save Interaction**.

---

# Environment Variables Reference

| Variable                     | Location          | Description                                      |
|-------------------------------|--------------------|---------------------------------------------------|
| `DATABASE_URL`                | backend/.env       | PostgreSQL connection string                       |
| `SECRET_KEY`                  | backend/.env       | JWT signing secret                                 |
| `ALGORITHM`                   | backend/.env       | JWT algorithm (default `HS256`)                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | backend/.env       | Token lifetime in minutes                          |
| `GROQ_API_KEY`                | backend/.env       | Your Groq API key                                  |
| `GROQ_MODEL`                  | backend/.env       | `gemma2-9b-it` or `llama-3.3-70b-versatile`        |
| `FRONTEND_ORIGIN`             | backend/.env       | Allowed CORS origin                                |
| `VITE_API_BASE_URL`           | frontend/.env      | Backend base URL used by Axios                     |

---

# API Endpoints Summary

| Method | Endpoint                       | Description                        |
|--------|---------------------------------|-------------------------------------|
| POST   | `/api/auth/register`            | Register a new user                 |
| POST   | `/api/auth/login`                | Login, returns JWT                  |
| GET    | `/api/hcps/`                     | List / search HCPs                  |
| POST   | `/api/hcps/`                     | Create HCP                          |
| GET/PUT/DELETE | `/api/hcps/{id}`          | Get / update / delete HCP            |
| GET    | `/api/interactions/`             | List interactions                   |
| POST   | `/api/interactions/`             | Create interaction                  |
| GET/PUT/DELETE | `/api/interactions/{id}`  | Get / update / delete interaction    |
| GET    | `/api/search/interactions`       | Structured filter search             |
| GET    | `/api/dashboard/stats`           | Aggregated dashboard stats           |
| POST   | `/api/chat/`                     | **LangGraph AI assistant endpoint**  |

---

#  Running Both Servers Together

Open two terminals:

# Terminal 1
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev


## 11. Notes on Code Quality

- Clean, layered architecture: `routers → services/crud → models`.
- LangGraph logic isolated in `app/langgraph_agent/`, fully decoupled from FastAPI request objects.
- All LLM calls funnel through a single `get_llm()` factory for one-line model switching.
- Comments included where logic isn't self-evident; no dead code, no TODOs, no placeholders.
