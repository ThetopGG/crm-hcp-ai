"""Dashboard / insights stats endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_user
from app.services.dashboard_service import get_dashboard_stats
from app.schemas.interaction import InteractionOut

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    stats = get_dashboard_stats(db)
    stats["recent_interactions"] = [InteractionOut.model_validate(i).model_dump(mode="json") for i in stats["recent_interactions"]]
    return stats
