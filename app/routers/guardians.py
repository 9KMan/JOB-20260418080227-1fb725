from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Guardian
from app.schemas import GuardianCreate, GuardianUpdate, GuardianResponse

router = APIRouter(prefix="/guardians", tags=["guardians"])


@router.post("", response_model=GuardianResponse, status_code=status.HTTP_201_CREATED)
def create_guardian(guardian: GuardianCreate, db: Session = Depends(get_db)):
    db_guardian = Guardian(**guardian.model_dump())
    db.add(db_guardian)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian


@router.get("", response_model=List[GuardianResponse])
def list_guardians(skip: int = 0, limit: int = 100, student_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Guardian)
    if student_id:
        query = query.filter(Guardian.student_id == student_id)
    guardians = query.offset(skip).limit(limit).all()
    return guardians


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_guardian(guardian_id: int, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.id == guardian_id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return guardian


@router.put("/{guardian_id}", response_model=GuardianResponse)
def update_guardian(guardian_id: int, guardian: GuardianUpdate, db: Session = Depends(get_db)):
    db_guardian = db.query(Guardian).filter(Guardian.id == guardian_id).first()
    if not db_guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")
    for key, value in guardian.model_dump(exclude_unset=True).items():
        setattr(db_guardian, key, value)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian


@router.delete("/{guardian_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guardian(guardian_id: int, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.id == guardian_id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian not found")
    db.delete(guardian)
    db.commit()
    return None