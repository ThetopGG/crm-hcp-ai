"""
Builds and compiles the actual LangGraph StateGraph for the CRM AI assistant.

Graph topology:

    START -> intent_detection -> decision -> tool_node -> llm_response -> database -> response -> END

Because each request needs its own DB session and current user, `build_graph`
takes those as arguments and binds them into the node functions with
functools.partial before adding them to the graph. This keeps nodes.py
free of any FastAPI/DB coupling in their core logic while still satisfying
LangGraph's `(state) -> dict` node signature.
"""
from functools import partial
from langgraph.graph import StateGraph, END

from app.langgraph_agent.state import AgentState
from app.langgraph_agent import nodes
from app.services.llm_service import get_llm


def build_graph(db, user_id: int):
    llm = get_llm()

    graph = StateGraph(AgentState)

    graph.add_node("intent_detection", partial(nodes.intent_detection_node, llm=llm))
    graph.add_node("decision", nodes.decision_node)
    graph.add_node("tool_node", partial(nodes.tool_node, db=db, llm=llm, user_id=user_id))
    graph.add_node("llm_response", partial(nodes.llm_response_node, llm=llm))
    graph.add_node("database", nodes.database_node)
    graph.add_node("response", nodes.response_node)

    graph.set_entry_point("intent_detection")
    graph.add_edge("intent_detection", "decision")
    graph.add_edge("decision", "tool_node")
    graph.add_edge("tool_node", "llm_response")
    graph.add_edge("llm_response", "database")
    graph.add_edge("database", "response")
    graph.add_edge("response", END)

    return graph.compile()


def run_agent(db, user_id: int, user_input: str, hcp_id: int | None = None, interaction_id: int | None = None) -> dict:
    """Convenience entry point used by the chat router."""
    compiled_graph = build_graph(db, user_id)

    initial_state: AgentState = {
        "user_input": user_input,
        "hcp_id": hcp_id,
        "interaction_id": interaction_id,
    }

    final_state = compiled_graph.invoke(initial_state)
    return final_state["final_response"]
