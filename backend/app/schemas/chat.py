"""Pydantic schemas for the AI chat / LangGraph endpoint."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatMessageIn(BaseModel):
    message: str
    # Optional currently-selected HCP id to give the agent context
    hcp_id: Optional[int] = None
    # Optional existing interaction id if the user is editing rather than creating
    interaction_id: Optional[int] = None


class ExtractedForm(BaseModel):
    doctor_name: Optional[str] = None
    speciality: Optional[str] = None
    hospital: Optional[str] = None
    interaction_date: Optional[str] = None
    interaction_type: Optional[str] = None
    products_discussed: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_date: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    intent: str
    extracted_form: Optional[ExtractedForm] = None
    tool_used: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
