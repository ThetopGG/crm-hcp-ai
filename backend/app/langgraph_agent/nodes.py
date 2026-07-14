"""
Node functions for the LangGraph agent.

Graph flow implemented here:

    User Input -> Intent Detection -> Decision Node -> Tool Node -> LLM -> Database -> Response

Each node is a plain function of (state) -> partial_state_update, as required
by LangGraph. Because nodes need access to the DB session, the current user,
and the LLM client, `graph.py` binds these via functools.partial when building
the graph per-request.
"""
from langchain_core.messages import SystemMessage, HumanMessage

from app.utils.json_parser import extract_json
from app.langgraph_agent.state import AgentState
from app.langgraph_agent.tools import (
    log_interaction_tool,
    edit_interaction_tool,
    search_interaction_tool,
    followup_tool,
    insights_tool,
)

VALID_INTENTS = ["log_interaction", "edit_interaction", "search_interaction", "follow_up", "insights", "general"]

INTENT_PROMPT = """Classify the field rep's message into exactly one of these intents:

- log_interaction: describing a new meeting/call/visit with a doctor that should be recorded
- edit_interaction: asking to change/correct/update an existing logged interaction
- search_interaction: asking to find/search/show past interactions
- follow_up: asking to generate a follow-up plan, agenda, or email for an existing interaction
- insights: asking for CRM analytics, stats, trends, or summaries across interactions
- general: anything else (greetings, small talk, unclear requests)

Respond with ONLY a JSON object: {{"intent": "<one_of_the_above>"}}

Message: \"\"\"{message}\"\"\"
"""


# ---------------------------------------------------------------------------
# NODE 1: Intent Detection
# ---------------------------------------------------------------------------
def intent_detection_node(state: AgentState, llm) -> dict:
    message = state["user_input"]
    response = llm.invoke([
        SystemMessage(content="You classify user intent. Reply with JSON only."),
        HumanMessage(content=INTENT_PROMPT.format(message=message)),
    ])
    data = extract_json(response.content)
    intent = data.get("intent", "general")
    if intent not in VALID_INTENTS:
        intent = "general"
    return {"intent": intent}


# ---------------------------------------------------------------------------
# NODE 2: Decision Node
# ---------------------------------------------------------------------------
def decision_node(state: AgentState) -> dict:
    """
    Maps the detected intent to a concrete tool, and validates that any
    required IDs (interaction_id) are present for tools that need them.
    Falls back to 'log_interaction' when an edit/follow_up is requested
    without a target id (treated as a new log instead).
    """
    intent = state.get("intent", "general")

    if intent == "edit_interaction" and not state.get("interaction_id"):
        return {"tool_to_use": "log_interaction"}

    if intent == "follow_up" and not state.get("interaction_id"):
        return {"tool_to_use": "log_interaction"}

    mapping = {
        "log_interaction": "log_interaction",
        "edit_interaction": "edit_interaction",
        "search_interaction": "search_interaction",
        "follow_up": "follow_up",
        "insights": "insights",
        "general": "none",
    }
    return {"tool_to_use": mapping.get(intent, "none")}


# ---------------------------------------------------------------------------
# NODE 3: Tool Node
# ---------------------------------------------------------------------------
def tool_node(state: AgentState, db, llm, user_id: int) -> dict:
    tool = state.get("tool_to_use", "none")
    message = state["user_input"]

    if tool == "log_interaction":
        result = log_interaction_tool.run(db, llm, user_id, message)
    elif tool == "edit_interaction":
        result = edit_interaction_tool.run(db, llm, state.get("interaction_id"), message)
    elif tool == "search_interaction":
        result = search_interaction_tool.run(db, llm, message)
    elif tool == "follow_up":
        result = followup_tool.run(db, llm, state.get("interaction_id"), message)
    elif tool == "insights":
        result = insights_tool.run(db, llm, message)
    else:
        result = {}

    return {"tool_used": tool, "tool_result": result, "extracted_form": result.get("extracted_form", {})}


# ---------------------------------------------------------------------------
# NODE 4: LLM Node (generates the final conversational reply to the rep)
# ---------------------------------------------------------------------------
def llm_response_node(state: AgentState, llm) -> dict:
    tool = state.get("tool_used", "none")
    result = state.get("tool_result", {})

    if tool == "none":
        response = llm.invoke([
            SystemMessage(content="You are a friendly pharma CRM AI assistant. Keep replies short and helpful."),
            HumanMessage(content=state["user_input"]),
        ])
        return {"reply": response.content.strip()}

    summary_prompt = f"""You are a CRM AI assistant. A tool named '{tool}' was just executed with this result (JSON):
{result}

Write a short, friendly 1-3 sentence reply to the field rep confirming what happened and, if relevant,
what to do next (e.g. review the auto-filled form and click Save). Plain text only."""

    response = llm.invoke([
        SystemMessage(content="You write short, friendly confirmations for CRM actions."),
        HumanMessage(content=summary_prompt),
    ])
    return {"reply": response.content.strip()}


# ---------------------------------------------------------------------------
# NODE 5: Database Node (confirms persistence outcome)
# ---------------------------------------------------------------------------
def database_node(state: AgentState) -> dict:
    result = state.get("tool_result", {})
    record_id = result.get("interaction_id") or result.get("follow_up_id")
    saved = bool(record_id) and "error" not in result
    return {"db_saved": saved, "db_record_id": record_id}


# ---------------------------------------------------------------------------
# NODE 6: Response Node (assembles the final API payload)
# ---------------------------------------------------------------------------
def response_node(state: AgentState) -> dict:
    final_response = {
        "reply": state.get("reply", ""),
        "intent": state.get("intent", "general"),
        "tool_used": state.get("tool_used", "none"),
        "extracted_form": state.get("extracted_form", {}),
        "data": state.get("tool_result", {}),
        "db_saved": state.get("db_saved", False),
        "db_record_id": state.get("db_record_id"),
    }
    return {"final_response": final_response}
