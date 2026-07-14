# Video Demo Script — AI-First CRM HCP Module
### Target length: 10–15 minutes

---

## 1. Introduction (0:00 – 1:00)

> "Hi, in this walkthrough I'll demo the AI-First CRM HCP Module — a CRM tool built for pharmaceutical field representatives. The core idea: instead of filling out long forms after every doctor visit, a rep can just describe what happened in plain language, and an AI agent — built with LangGraph — extracts the structured data, fills the form, and saves it to the database automatically."

Mention the stack briefly: React + Redux Toolkit + MUI on the frontend, FastAPI + SQLAlchemy + PostgreSQL on the backend, and a LangGraph agent powered by Groq's LLM API.

---

## 2. Architecture Walkthrough (1:00 – 3:00)

Show the architecture diagram from the README. Explain the flow:

> "Every message the rep sends goes through a LangGraph graph with six nodes: Intent Detection, Decision, Tool Node, LLM, Database, and Response. The Intent Detection node classifies what the rep wants — logging a new interaction, editing one, searching, generating a follow-up, or getting insights. The Decision node picks the right tool. The Tool node actually does the work — calling the LLM for extraction and touching the database. Then a final LLM node writes a friendly confirmation message back to the rep."

Open `backend/app/langgraph_agent/graph.py` and `nodes.py` briefly on screen to show the real `StateGraph` code — emphasize this is **not** a hardcoded if/else chain, it's an actual LangGraph graph.

---

## 3. Login / Register (3:00 – 4:00)

- Open the app at `localhost:5173`.
- Show the Login screen, switch to the Register tab.
- Register a new field rep account.
- Show automatic redirect to the Dashboard after registration.

---

## 4. Dashboard (4:00 – 5:30)

- Point out the four stat cards: Total HCPs, Total Interactions, Pending Follow-ups, Overdue Follow-ups.
- Show the Recent Interactions list and Top Products Discussed chips.
- Explain these numbers come from the `/api/dashboard/stats` endpoint, powered by the `dashboard_service` aggregation logic and — when asked in the chat — the `insights_tool` LangGraph tool.

---

## 5. HCP List (5:30 – 6:30)

- Navigate to HCP List.
- Show the search bar filtering by name/hospital/speciality.
- Add a new HCP manually via the "Add HCP" dialog to show manual CRUD works alongside the AI flow.

---

## 6. Log Interaction — The Core Demo (6:30 – 11:00)

This is the centerpiece — spend the most time here.

1. Navigate to **Log Interaction**. Show the two-panel layout: structured form on the left, AI Assistant chat on the right.
2. Type into the chat:
   > "I met Dr Sharma today at Apollo Hospital. We discussed CardX. He wants efficacy data next Monday."
3. Show the AI's reply appear, and the structured form auto-fill: Doctor Name, Hospital, Products Discussed, Follow-up Date all populated.
4. Explain what happened under the hood:
   - Intent Detection classified this as `log_interaction`.
   - The Decision node routed to the `log_interaction_tool`.
   - The tool called the Groq LLM to extract entities into JSON, created (or reused) the HCP record, and saved a new Interaction row — all before the reply was even shown.
5. Adjust a field manually (e.g. tweak the Notes), then click **Save Interaction** to show the manual save/update path also works.
6. Try a follow-up chat message:
   > "Generate a follow-up email for this."
   Show the `followup_tool` in action — agenda + email draft returned in the AI's reply.
7. Try a search query:
   > "Show me all interactions about CardX"
   Show the `search_interaction_tool` extracting filters and returning results.
8. Try an insights query:
   > "Give me insights on my CRM activity"
   Show the `insights_tool` narrative response.

---

## 7. Interaction History (11:00 – 12:30)

- Navigate to Interaction History.
- Show the table of all logged interactions, including the one just created.
- Use the Doctor / Product / Keyword filters to demonstrate the `/api/search/interactions` endpoint.

---

## 8. Settings (12:30 – 13:15)

- Show the Settings page: profile info (read-only) and the AI Configuration card explaining the Groq model in use and how to switch models.

---

## 9. Code Quality & Wrap-up (13:15 – 15:00)

- Briefly show the backend folder structure: routers, services, crud, models, schemas, langgraph_agent.
- Emphasize: no placeholders, no TODOs, fully working end-to-end.
- Mention the one-line model switch: changing `GROQ_MODEL` in `.env` from `gemma2-9b-it` to `llama-3.3-70b-versatile` — no other code changes required.
- Close with a summary of what was built and how it satisfies the assignment requirements: five real LangGraph tools, the exact required graph flow, a two-panel Log Interaction screen, full CRUD, and a professional pharma CRM UI.

> "That's the AI-First CRM HCP Module — thanks for watching!"
