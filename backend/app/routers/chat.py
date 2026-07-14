"""
AI Chat / LangGraph endpoint.

This is the endpoint that powers the AI Assistant chat panel on the
Log Interaction screen. Every message is routed through the LangGraph
agent (see app/langgraph_agent/graph.py), which detects intent, decides
which tool to invoke, runs the tool (extraction + DB read/write), asks
the LLM for a friendly confirmation reply, and returns a structured
response the frontend can use to auto-fill the form.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_user
from app.schemas.chat import ChatMessageIn, ChatResponse
from app.langgraph_agent.graph import run_agent

router = APIRouter(prefix="/api/chat", tags=["AI Chat"])


@router.post("/", response_model=ChatResponse)
def chat(payload: ChatMessageIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = run_agent(
        db=db,
        user_id=user.id,
        user_input=payload.message,
        hcp_id=payload.hcp_id,
        interaction_id=payload.interaction_id,
    )

    return ChatResponse(
        reply=result.get("reply", ""),
        intent=result.get("intent", "general"),
        extracted_form=result.get("extracted_form") or None,
        tool_used=result.get("tool_used"),
        data=result.get("data"),
    )
