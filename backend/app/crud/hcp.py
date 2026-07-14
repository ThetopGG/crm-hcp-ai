"""CRUD operations for HCP."""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate


def get_hcp(db: Session, hcp_id: int):
    return db.query(HCP).filter(HCP.id == hcp_id).first()


def get_hcp_by_name(db: Session, name: str):
    return db.query(HCP).filter(HCP.name.ilike(name)).first()


def list_hcps(db: Session, search: str | None = None, skip: int = 0, limit: int = 100):
    query = db.query(HCP)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(HCP.name.ilike(like), HCP.hospital.ilike(like), HCP.speciality.ilike(like)))
    return query.order_by(HCP.name).offset(skip).limit(limit).all()


def create_hcp(db: Session, hcp_in: HCPCreate) -> HCP:
    hcp = HCP(**hcp_in.model_dump())
    db.add(hcp)
    db.commit()
    db.refresh(hcp)
    return hcp


def get_or_create_hcp(db: Session, name: str, speciality: str | None = None, hospital: str | None = None) -> HCP:
    """Used by the AI pipeline: find an HCP by name or create a new one on the fly."""
    hcp = get_hcp_by_name(db, name)
    if hcp:
        # Enrich missing fields if the AI extracted new info
        updated = False
        if speciality and not hcp.speciality:
            hcp.speciality = speciality
            updated = True
        if hospital and not hcp.hospital:
            hcp.hospital = hospital
            updated = True
        if updated:
            db.commit()
            db.refresh(hcp)
        return hcp

    hcp = HCP(name=name, speciality=speciality, hospital=hospital)
    db.add(hcp)
    db.commit()
    db.refresh(hcp)
    return hcp


def update_hcp(db: Session, hcp: HCP, hcp_in: HCPUpdate) -> HCP:
    for field, value in hcp_in.model_dump(exclude_unset=True).items():
        setattr(hcp, field, value)
    db.commit()
    db.refresh(hcp)
    return hcp


def delete_hcp(db: Session, hcp: HCP):
    db.delete(hcp)
    db.commit()
