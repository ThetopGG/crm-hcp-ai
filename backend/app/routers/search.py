"""Direct (non-AI) search endpoint for interactions - used by the History page filters."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_db
from app.core.deps import get_current_user
from app.schemas.interaction import InteractionSearchResult
from app.crud.interaction import search_interactions

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/interactions", response_model=InteractionSearchResult)
def search(
    doctor: Optional[str] = None,
    product: Optional[str] = None,
    keyword: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    results = search_interactions(db, doctor=doctor, product=product, keyword=keyword, date_from=date_from, date_to=date_to)
    return {"results": results, "count": len(results)}
