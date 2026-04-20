from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import School
from app.schemas import SchoolCreate, SchoolUpdate, SchoolResponse

router = APIRouter(prefix="/schools", tags=["schools"])


@router.post("", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    db_school = School(**school.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


@router.get("", response_model=List[SchoolResponse])
def list_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schools = db.query(School).offset(skip).limit(limit).all()
    return schools


@router.get("/{school_id}", response_model=SchoolResponse)
def get_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.put("/{school_id}", response_model=SchoolResponse)
def update_school(school_id: int, school: SchoolUpdate, db: Session = Depends(get_db)):
    db_school = db.query(School).filter(School.id == school_id).first()
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    for key, value in school.model_dump(exclude_unset=True).items():
        setattr(db_school, key, value)
    db.commit()
    db.refresh(db_school)
    return db_school


@router.post("/{school_id}/verify", response_model=SchoolResponse)
def verify_school(school_id: int, db: Session = Depends(get_db)):
    from datetime import datetime
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    school.verification_status = "verified"
    school.verified_at = datetime.utcnow()
    db.commit()
    db.refresh(school)
    return school


@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    db.delete(school)
    db.commit()
    return None