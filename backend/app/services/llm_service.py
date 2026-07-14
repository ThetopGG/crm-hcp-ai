"""
Thin wrapper around the Groq-hosted LLM via langchain-groq.

Changing GROQ_MODEL in .env (or app/config.py) is the ONLY thing required
to switch from gemma2-9b-it to llama-3.3-70b-versatile - every node/tool
in the LangGraph agent imports `get_llm()` from this module instead of
instantiating its own client.
"""
from langchain_groq import ChatGroq
from app.config import settings


def get_llm(temperature: float = 0.2):
    """Returns a configured ChatGroq LLM client using the model set in settings.GROQ_MODEL."""
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=temperature,
    )
