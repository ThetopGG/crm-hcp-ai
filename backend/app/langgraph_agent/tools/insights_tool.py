"""
TOOL 5: Insights Tool

Generates CRM insights such as interaction frequency, pending follow-ups,
most-discussed products, and doctor engagement levels. Uses the dashboard
aggregation service for the numbers, then asks the LLM to turn them into
a short natural-language insight summary for the rep.
"""
from sqlalchemy.orm import Session
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy import func

from app.services.dashboard_service import get_dashboard_stats
from app.models.interaction import Interaction
from app.models.hcp import HCP

INSIGHTS_PROMPT = """You are a CRM analytics assistant for a pharmaceutical field rep.

Here is the current CRM data summary (JSON):
{stats}

Write a short (3-5 sentence) natural-language insight summary highlighting:
- overall activity level
- pending/overdue follow-ups that need attention
- top products being discussed
- any doctor engagement pattern worth noting

Respond with plain text only (no JSON, no markdown headers).
"""


def run(db: Session, llm, message: str = "") -> dict:
    stats = get_dashboard_stats(db)

    # doctor engagement: interaction count per doctor
    engagement = (
        db.query(HCP.name, func.count(Interaction.id).label("cnt"))
        .join(Interaction, Interaction.hcp_id == HCP.id)
        .group_by(HCP.name)
        .order_by(func.count(Interaction.id).desc())
        .limit(5)
        .all()
    )

    stats_for_llm = {
        "total_hcps": stats["total_hcps"],
        "total_interactions": stats["total_interactions"],
        "pending_follow_ups": stats["pending_follow_ups"],
        "overdue_follow_ups": stats["overdue_follow_ups"],
        "top_products": stats["top_products"],
        "top_engaged_doctors": [{"doctor": name, "interactions": cnt} for name, cnt in engagement],
    }

    response = llm.invoke([
        SystemMessage(content="You are a helpful, concise pharma CRM analytics assistant."),
        HumanMessage(content=INSIGHTS_PROMPT.format(stats=stats_for_llm)),
    ])

    return {
        "narrative": response.content.strip(),
        "stats": stats_for_llm,
    }
