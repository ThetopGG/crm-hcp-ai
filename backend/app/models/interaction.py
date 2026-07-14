"""Interaction model - a logged meeting/call between a rep and an HCP."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    interaction_date = Column(Date, nullable=False)
    interaction_type = Column(String(50), nullable=False, default="Visit")  # Visit, Call, Email, Video
    products_discussed = Column(String(500), nullable=True)  # comma separated product names
    notes = Column(Text, nullable=True)
    outcome = Column(String(500), nullable=True)
    follow_up_date = Column(Date, nullable=True)

    raw_conversation = Column(Text, nullable=True)   # original free-text the rep typed to the AI
    ai_summary = Column(Text, nullable=True)         # AI generated summary

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    hcp = relationship("HCP", back_populates="interactions")
    created_by_user = relationship("User", back_populates="interactions")
    follow_ups = relationship("FollowUp", back_populates="interaction", cascade="all, delete-orphan")
