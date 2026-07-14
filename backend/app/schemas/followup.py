"""Pydantic schemas for follow-ups."""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class FollowUpBase(BaseModel):
    due_date: Optional[date] = None
    agenda: Optional[str] = None
    email_draft: Optional[str] = None
    summary: Optional[str] = None


class FollowUpCreate(FollowUpBase):
    interaction_id: int


class FollowUpOut(FollowUpBase):
    id: int
    interaction_id: int
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
