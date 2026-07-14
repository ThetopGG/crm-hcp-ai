"""Pydantic schemas for interactions."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from app.schemas.hcp import HCPOut
from app.schemas.followup import FollowUpOut


class InteractionBase(BaseModel):
    hcp_id: int
    interaction_date: date
    interaction_type: str = "Visit"
    products_discussed: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_date: Optional[date] = None


class InteractionCreate(InteractionBase):
    raw_conversation: Optional[str] = None
    ai_summary: Optional[str] = None


class InteractionUpdate(BaseModel):
    hcp_id: Optional[int] = None
    interaction_date: Optional[date] = None
    interaction_type: Optional[str] = None
    products_discussed: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_date: Optional[date] = None


class InteractionOut(InteractionBase):
    id: int
    created_by: int
    raw_conversation: Optional[str] = None
    ai_summary: Optional[str] = None
    created_at: datetime
    hcp: Optional[HCPOut] = None
    follow_ups: List[FollowUpOut] = []

    class Config:
        from_attributes = True


class InteractionSearchResult(BaseModel):
    results: List[InteractionOut]
    count: int
