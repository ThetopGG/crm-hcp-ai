"""Aggregation logic for the dashboard / insights views."""
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.interaction import Interaction
from app.models.hcp import HCP


def get_dashboard_stats(db: Session) -> dict:
    total_hcps = db.query(func.count(HCP.id)).scalar() or 0
    total_interactions = db.query(func.count(Interaction.id)).scalar() or 0

    pending_follow_ups = (
        db.query(func.count(Interaction.id))
        .filter(Interaction.follow_up_date.isnot(None))
        .filter(Interaction.follow_up_date >= date.today())
        .scalar()
        or 0
    )

    overdue_follow_ups = (
        db.query(func.count(Interaction.id))
        .filter(Interaction.follow_up_date.isnot(None))
        .filter(Interaction.follow_up_date < date.today())
        .scalar()
        or 0
    )

    recent_interactions = (
        db.query(Interaction)
        .order_by(Interaction.interaction_date.desc(), Interaction.id.desc())
        .limit(5)
        .all()
    )

    # Product mention frequency (simple split on comma)
    product_counter: dict[str, int] = {}
    for (products_discussed,) in db.query(Interaction.products_discussed).all():
        if not products_discussed:
            continue
        for p in products_discussed.split(","):
            p = p.strip()
            if p:
                product_counter[p] = product_counter.get(p, 0) + 1

    top_products = sorted(product_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total_hcps": total_hcps,
        "total_interactions": total_interactions,
        "pending_follow_ups": pending_follow_ups,
        "overdue_follow_ups": overdue_follow_ups,
        "recent_interactions": recent_interactions,
        "top_products": [{"product": p, "count": c} for p, c in top_products],
    }
