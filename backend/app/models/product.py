"""Product model - pharmaceutical products discussed with HCPs."""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
