"""
FastAPI application entrypoint for the AI-First CRM HCP Module backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.config import settings

# Import models so SQLAlchemy metadata knows about every table before create_all
from app import models  # noqa: F401

from app.routers import auth, hcp, interaction, search, dashboard, chat

# Create all tables (for local/dev use). In production, prefer Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM HCP Module API",
    description="Backend API for the pharmaceutical field rep CRM with a LangGraph-powered AI assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(hcp.router)
app.include_router(interaction.router)
app.include_router(search.router)
app.include_router(dashboard.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "crm-hcp-ai backend", "model": settings.GROQ_MODEL}


@app.get("/health")
def health():
    return {"status": "healthy"}
