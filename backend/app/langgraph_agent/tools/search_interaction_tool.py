"""
TOOL 3: Search Interaction

Lets the rep search past interactions by doctor name, date, product, or
free-text keyword using natural language, e.g.
"Show me all meetings with Dr Sharma about CardX last month".

The LLM extracts structured filters from the natural language query,
which are then used to run a SQL search via crud.search_interactions.
"""
from sqlalchemy.orm import Session
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import date

from app.utils.json_parser import extract_json
from app.crud.interaction import search_interactions

SEARCH_PROMPT = """Extract search filters from the field rep's request about past CRM interactions.

Respond with ONLY a JSON object with these keys (use null if not mentioned):
{{
  "doctor": string or null,
  "product": string or null,
  "keyword": string or null,
  "date_from": "YYYY-MM-DD" or null,
  "date_to": "YYYY-MM-DD" or null
}}

Today's date is {today}.

Rep's request:
\"\"\"{message}\"\"\"
"""


def run(db: Session, llm, message: str) -> dict:
    today = date.today().isoformat()
    prompt = SEARCH_PROMPT.format(today=today, message=message)

    response = llm.invoke([
        SystemMessage(content="You output only valid JSON search filters."),
        HumanMessage(content=prompt),
    ])

    filters = extract_json(response.content)

    date_from = None
    date_to = None
    try:
        if filters.get("date_from"):
            date_from = date.fromisoformat(filters["date_from"])
        if filters.get("date_to"):
            date_to = date.fromisoformat(filters["date_to"])
    except ValueError:
        pass

    results = search_interactions(
        db,
        doctor=filters.get("doctor"),
        product=filters.get("product"),
        keyword=filters.get("keyword"),
        date_from=date_from,
        date_to=date_to,
    )

    return {
        "filters_used": filters,
        "count": len(results),
        "results": [
            {
                "id": r.id,
                "doctor_name": r.hcp.name if r.hcp else None,
                "interaction_date": r.interaction_date.isoformat(),
                "interaction_type": r.interaction_type,
                "products_discussed": r.products_discussed,
                "outcome": r.outcome,
                "follow_up_date": r.follow_up_date.isoformat() if r.follow_up_date else None,
            }
            for r in results
        ],
    }
