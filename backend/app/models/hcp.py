"""HCP model - Health Care Professional (Doctor) that a rep interacts with."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    speciality = Column(String(150), nullable=True)
    hospital = Column(String(200), nullable=True)
    phone = Column(String(30), nullable=True)
    email = Column(String(150), nullable=True)
    city = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interactions = relationship("Interaction", back_populates="hcp", cascade="all, delete-orphan")
