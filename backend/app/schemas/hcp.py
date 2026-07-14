"""Pydantic schemas for HCP (doctor) records."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HCPBase(BaseModel):
    name: str
    speciality: Optional[str] = None
    hospital: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None


class HCPCreate(HCPBase):
    pass


class HCPUpdate(BaseModel):
    name: Optional[str] = None
    speciality: Optional[str] = None
    hospital: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None


class HCPOut(HCPBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
