"""
TOOL 2: Edit Interaction

Allows the rep to modify an existing interaction using natural language,
e.g. "Actually the follow-up should be next Friday, not Monday."

Uses the LLM to figure out which fields changed, then applies a partial
update to the existing Interaction record.
"""
from datetime import date
from sqlalchemy.orm import Session
from langchain_core.messages import SystemMessage, HumanMessage

from app.utils.json_parser import extract_json
from app.crud.interaction import get_interaction, update_interaction
from app.schemas.interaction import InteractionUpdate

EDIT_PROMPT = """You are a CRM assistant. The field rep wants to EDIT an existing interaction record.

Current record (JSON):
{current}

The rep's edit instruction:
\"\"\"{message}\"\"\"

Respond with ONLY a JSON object containing ONLY the fields that should change, using these possible keys:
interaction_type, products_discussed, notes, outcome, follow_up_date ("YYYY-MM-DD"), interaction_date ("YYYY-MM-DD").
Today's date is {today}. If nothing should change for a field, omit that key entirely.
"""


def run(db: Session, llm, interaction_id: int, message: str) -> dict:
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        return {"error": f"Interaction {interaction_id} not found"}

    current = {
        "interaction_type": interaction.interaction_type,
        "products_discussed": interaction.products_discussed,
        "notes": interaction.notes,
        "outcome": interaction.outcome,
        "follow_up_date": interaction.follow_up_date.isoformat() if interaction.follow_up_date else None,
        "interaction_date": interaction.interaction_date.isoformat(),
    }

    today = date.today().isoformat()
    prompt = EDIT_PROMPT.format(current=current, message=message, today=today)

    response = llm.invoke([
        SystemMessage(content="You output only valid JSON representing a partial update."),
        HumanMessage(content=prompt),
    ])

    changes = extract_json(response.content)

    for date_field in ("follow_up_date", "interaction_date"):
        if changes.get(date_field):
            try:
                changes[date_field] = date.fromisoformat(changes[date_field])
            except ValueError:
                changes.pop(date_field, None)

    update_schema = InteractionUpdate(**changes)
    updated = update_interaction(db, interaction, update_schema)

    return {
        "interaction_id": updated.id,
        "updated_fields": list(changes.keys()),
        "current_state": {
            "interaction_type": updated.interaction_type,
            "products_discussed": updated.products_discussed,
            "notes": updated.notes,
            "outcome": updated.outcome,
            "follow_up_date": updated.follow_up_date.isoformat() if updated.follow_up_date else None,
            "interaction_date": updated.interaction_date.isoformat(),
        },
    }
