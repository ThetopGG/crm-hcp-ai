"""FollowUp model - AI-generated or manually created follow-up tasks tied to an interaction."""
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)

    due_date = Column(Date, nullable=True)
    agenda = Column(Text, nullable=True)
    email_draft = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("Interaction", back_populates="follow_ups")
