"""HCP (doctor) CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.core.deps import get_current_user
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPOut
from app.crud import hcp as hcp_crud

router = APIRouter(prefix="/api/hcps", tags=["HCP"])


@router.get("/", response_model=List[HCPOut])
def list_hcps(search: Optional[str] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return hcp_crud.list_hcps(db, search=search)


@router.post("/", response_model=HCPOut)
def create_hcp(hcp_in: HCPCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return hcp_crud.create_hcp(db, hcp_in)


@router.get("/{hcp_id}", response_model=HCPOut)
def get_hcp(hcp_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    hcp = hcp_crud.get_hcp(db, hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp


@router.put("/{hcp_id}", response_model=HCPOut)
def update_hcp(hcp_id: int, hcp_in: HCPUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    hcp = hcp_crud.get_hcp(db, hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp_crud.update_hcp(db, hcp, hcp_in)


@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    hcp = hcp_crud.get_hcp(db, hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    hcp_crud.delete_hcp(db, hcp)
    return {"detail": "HCP deleted"}
