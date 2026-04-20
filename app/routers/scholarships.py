from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Scholarship
from app.schemas import ScholarshipCreate, ScholarshipUpdate, ScholarshipResponse

router = APIRouter(prefix="/scholarships", tags=["scholarships"])


@router.post("", response_model=ScholarshipResponse, status_code=status.HTTP_201_CREATED)
def create_scholarship(scholarship: ScholarshipCreate, db: Session = Depends(get_db)):
    db_scholarship = Scholarship(
        student_id=scholarship.student_id,
        agent_id=scholarship.agent_id,
        items=[item.model_dump() for item in scholarship.items],
        total_amount=scholarship.total_amount
    )
    db.add(db_scholarship)
    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship


@router.get("", response_model=List[ScholarshipResponse])
def list_scholarships(skip: int = 0, limit: int = 100, student_id: int = None, status: str = None, db: Session = Depends(get_db)):
    query = db.query(Scholarship)
    if student_id:
        query = query.filter(Scholarship.student_id == student_id)
    if status:
        query = query.filter(Scholarship.status == status)
    scholarships = query.order_by(Scholarship.created_at.desc()).offset(skip).limit(limit).all()
    return scholarships


@router.get("/{scholarship_id}", response_model=ScholarshipResponse)
def get_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship


@router.put("/{scholarship_id}", response_model=ScholarshipResponse)
def update_scholarship(scholarship_id: int, scholarship: ScholarshipUpdate, db: Session = Depends(get_db)):
    db_scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not db_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    update_data = scholarship.model_dump(exclude_unset=True)
    if "items" in update_data:
        update_data["items"] = [item.model_dump() if hasattr(item, 'model_dump') else item for item in update_data["items"]]
    for key, value in update_data.items():
        setattr(db_scholarship, key, value)
    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship


@router.delete("/{scholarship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    db.delete(scholarship)
    db.commit()
    return None