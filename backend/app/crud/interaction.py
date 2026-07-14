"""CRUD operations for Interaction and FollowUp."""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.interaction import Interaction
from app.models.followup import FollowUp
from app.models.hcp import HCP
from app.schemas.interaction import InteractionCreate, InteractionUpdate


def get_interaction(db: Session, interaction_id: int):
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def list_interactions(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Interaction)
        .order_by(Interaction.interaction_date.desc(), Interaction.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_interaction(db: Session, interaction_in: InteractionCreate, user_id: int) -> Interaction:
    interaction = Interaction(
        hcp_id=interaction_in.hcp_id,
        created_by=user_id,
        interaction_date=interaction_in.interaction_date,
        interaction_type=interaction_in.interaction_type,
        products_discussed=interaction_in.products_discussed,
        notes=interaction_in.notes,
        outcome=interaction_in.outcome,
        follow_up_date=interaction_in.follow_up_date,
        raw_conversation=interaction_in.raw_conversation,
        ai_summary=interaction_in.ai_summary,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def update_interaction(db: Session, interaction: Interaction, interaction_in: InteractionUpdate) -> Interaction:
    for field, value in interaction_in.model_dump(exclude_unset=True).items():
        setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


def delete_interaction(db: Session, interaction: Interaction):
    db.delete(interaction)
    db.commit()


def search_interactions(
    db: Session,
    doctor: str | None = None,
    product: str | None = None,
    keyword: str | None = None,
    date_from=None,
    date_to=None,
):
    query = db.query(Interaction).join(HCP, Interaction.hcp_id == HCP.id)

    if doctor:
        query = query.filter(HCP.name.ilike(f"%{doctor}%"))
    if product:
        query = query.filter(Interaction.products_discussed.ilike(f"%{product}%"))
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            or_(
                Interaction.notes.ilike(like),
                Interaction.outcome.ilike(like),
                Interaction.ai_summary.ilike(like),
                Interaction.raw_conversation.ilike(like),
            )
        )
    if date_from:
        query = query.filter(Interaction.interaction_date >= date_from)
    if date_to:
        query = query.filter(Interaction.interaction_date <= date_to)

    return query.order_by(Interaction.interaction_date.desc()).all()


def create_follow_up(db: Session, interaction_id: int, due_date=None, agenda=None, email_draft=None, summary=None) -> FollowUp:
    follow_up = FollowUp(
        interaction_id=interaction_id,
        due_date=due_date,
        agenda=agenda,
        email_draft=email_draft,
        summary=summary,
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return follow_up
