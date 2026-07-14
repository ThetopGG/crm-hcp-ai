"""
TOOL 1: Log Interaction

Takes the rep's free-text description of a meeting/call, uses the LLM to:
  - summarize the conversation
  - extract structured entities (doctor, hospital, products, outcome, follow-up date, etc.)
  - convert it into structured JSON
  - persist a new HCP (if needed) and Interaction record to the database

Returns a dict with the extracted form fields, the AI summary, and the
created interaction id so the frontend structured form can be auto-filled
and the user can review/edit before final save.
"""
from datetime import date
from sqlalchemy.orm import Session
from langchain_core.messages import SystemMessage, HumanMessage

from app.utils.json_parser import extract_json
from app.crud.hcp import get_or_create_hcp
from app.crud.interaction import create_interaction
from app.schemas.interaction import InteractionCreate

EXTRACTION_PROMPT = """You are a CRM assistant for pharmaceutical field representatives.
A field rep will describe a meeting or call with a doctor in free text.

Extract the information and respond with ONLY a JSON object (no markdown, no explanation) with these exact keys:
{{
  "doctor_name": string or null,
  "speciality": string or null,
  "hospital": string or null,
  "interaction_date": "YYYY-MM-DD" or null (use today's date {today} if not mentioned),
  "interaction_type": one of ["Visit", "Call", "Email", "Video"] (default "Visit"),
  "products_discussed": comma separated string of product names or null,
  "notes": a concise 1-2 sentence note capturing what happened or null,
  "outcome": short description of the outcome/result of the interaction or null,
  "follow_up_date": "YYYY-MM-DD" or null (infer from phrases like "next Monday" relative to {today}),
  "summary": a professional 2-3 sentence summary of the interaction suitable for a CRM record
}}

Rep's message:
\"\"\"{message}\"\"\"
"""


def run(db: Session, llm, user_id: int, message: str) -> dict:
    today = date.today().isoformat()
    prompt = EXTRACTION_PROMPT.format(today=today, message=message)

    response = llm.invoke([
        SystemMessage(content="You are a precise data extraction engine. Always reply with valid JSON only."),
        HumanMessage(content=prompt),
    ])

    data = extract_json(response.content)

    doctor_name = data.get("doctor_name") or "Unknown Doctor"
    speciality = data.get("speciality")
    hospital = data.get("hospital")
    interaction_date_str = data.get("interaction_date") or today
    interaction_type = data.get("interaction_type") or "Visit"
    products_discussed = data.get("products_discussed")
    notes = data.get("notes")
    outcome = data.get("outcome")
    follow_up_date_str = data.get("follow_up_date")
    summary = data.get("summary") or notes or "Interaction logged via AI assistant."

    try:
        interaction_date = date.fromisoformat(interaction_date_str)
    except (ValueError, TypeError):
        interaction_date = date.today()

    follow_up_date = None
    if follow_up_date_str:
        try:
            follow_up_date = date.fromisoformat(follow_up_date_str)
        except ValueError:
            follow_up_date = None

    hcp = get_or_create_hcp(db, name=doctor_name, speciality=speciality, hospital=hospital)

    interaction_in = InteractionCreate(
        hcp_id=hcp.id,
        interaction_date=interaction_date,
        interaction_type=interaction_type,
        products_discussed=products_discussed,
        notes=notes,
        outcome=outcome,
        follow_up_date=follow_up_date,
        raw_conversation=message,
        ai_summary=summary,
    )
    interaction = create_interaction(db, interaction_in, user_id=user_id)

    extracted_form = {
        "doctor_name": hcp.name,
        "speciality": hcp.speciality,
        "hospital": hcp.hospital,
        "interaction_date": interaction_date.isoformat(),
        "interaction_type": interaction_type,
        "products_discussed": products_discussed,
        "notes": notes,
        "outcome": outcome,
        "follow_up_date": follow_up_date.isoformat() if follow_up_date else None,
    }

    return {
        "extracted_form": extracted_form,
        "summary": summary,
        "interaction_id": interaction.id,
        "hcp_id": hcp.id,
    }
