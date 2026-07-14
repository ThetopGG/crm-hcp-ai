"""
TOOL 4: Generate Follow-up

Given an interaction (and optional extra instruction from the rep), uses
the LLM to generate:
  - a next meeting agenda
  - a follow-up email draft to the doctor
  - a short follow-up summary

Persists the result as a FollowUp record linked to the interaction.
"""
from sqlalchemy.orm import Session
from langchain_core.messages import SystemMessage, HumanMessage

from app.utils.json_parser import extract_json
from app.crud.interaction import get_interaction, create_follow_up

FOLLOWUP_PROMPT = """You are a CRM assistant helping a pharmaceutical field rep prepare a follow-up.

Interaction details:
- Doctor: {doctor_name}
- Hospital: {hospital}
- Products discussed: {products}
- Notes: {notes}
- Outcome: {outcome}
- Follow-up date: {follow_up_date}

Extra instruction from rep (may be empty): "{message}"

Respond with ONLY a JSON object with these keys:
{{
  "agenda": "3-5 bullet point agenda for the next meeting, as a single string with \\n between bullets",
  "email_draft": "a polite, professional follow-up email to the doctor, including a subject line",
  "summary": "1-2 sentence summary of what the follow-up should accomplish"
}}
"""


def run(db: Session, llm, interaction_id: int, message: str = "") -> dict:
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        return {"error": f"Interaction {interaction_id} not found"}

    hcp = interaction.hcp
    prompt = FOLLOWUP_PROMPT.format(
        doctor_name=hcp.name if hcp else "Unknown",
        hospital=hcp.hospital if hcp else "Unknown",
        products=interaction.products_discussed or "None",
        notes=interaction.notes or "None",
        outcome=interaction.outcome or "None",
        follow_up_date=interaction.follow_up_date.isoformat() if interaction.follow_up_date else "Not set",
        message=message or "",
    )

    response = llm.invoke([
        SystemMessage(content="You output only valid JSON. You write professional pharma-industry correspondence."),
        HumanMessage(content=prompt),
    ])

    data = extract_json(response.content)
    agenda = data.get("agenda", "")
    email_draft = data.get("email_draft", "")
    summary = data.get("summary", "")

    follow_up = create_follow_up(
        db,
        interaction_id=interaction.id,
        due_date=interaction.follow_up_date,
        agenda=agenda,
        email_draft=email_draft,
        summary=summary,
    )

    return {
        "follow_up_id": follow_up.id,
        "agenda": agenda,
        "email_draft": email_draft,
        "summary": summary,
    }
