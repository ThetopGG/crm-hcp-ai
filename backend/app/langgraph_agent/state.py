"""
Shared state object passed between every node in the LangGraph graph.

LangGraph nodes receive this dict, return a partial dict of updates,
and LangGraph merges the updates back into the state for the next node.
"""
from typing import TypedDict, Optional, Dict, Any


class AgentState(TypedDict, total=False):
    # ---- input ----
    user_input: str
    hcp_id: Optional[int]
    interaction_id: Optional[int]

    # ---- intent detection ----
    intent: str  # one of: log_interaction, edit_interaction, search_interaction, follow_up, insights, general

    # ---- decision node ----
    tool_to_use: str

    # ---- tool node output ----
    tool_used: str
    tool_result: Dict[str, Any]
    extracted_form: Dict[str, Any]

    # ---- llm node output ----
    reply: str

    # ---- db node output ----
    db_saved: bool
    db_record_id: Optional[int]

    # ---- final response ----
    final_response: Dict[str, Any]
