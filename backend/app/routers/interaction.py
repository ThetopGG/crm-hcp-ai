"""Interaction CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.deps import get_current_user
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionOut
from app.crud import interaction as interaction_crud

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])


@router.get("/", response_model=List[InteractionOut])
def list_interactions(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return interaction_crud.list_interactions(db)


@router.post("/", response_model=InteractionOut)
def create_interaction(interaction_in: InteractionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return interaction_crud.create_interaction(db, interaction_in, user_id=user.id)


@router.get("/{interaction_id}", response_model=InteractionOut)
def get_interaction(interaction_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    interaction = interaction_crud.get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.put("/{interaction_id}", response_model=InteractionOut)
def update_interaction(interaction_id: int, interaction_in: InteractionUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    interaction = interaction_crud.get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction_crud.update_interaction(db, interaction, interaction_in)


@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    interaction = interaction_crud.get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    interaction_crud.delete_interaction(db, interaction)
    return {"detail": "Interaction deleted"}
