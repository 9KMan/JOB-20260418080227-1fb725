from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Payment, Scholarship, Student, School
from app.schemas import PaymentCreate, PaymentInitiate, PaymentResponse, PaymentVerifyResponse
from app.services.paystack import paystack_service
from app.services.flutterwave import flutterwave_service
from app.services.interac import interac_service
from app.services.receipt import receipt_service

router = APIRouter(prefix="/payments", tags=["payments"])


async def _get_student_name(student: Student) -> str:
    return student.name if student else "Unknown"


async def _check_school_verified(db: Session, scholarship: Scholarship) -> None:
    """Raise 403 if the school linked to scholarship is not verified."""
    student = db.query(Student).filter(Student.id == scholarship.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    school = db.query(School).filter(School.id == student.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    if school.verification_status != "verified":
        raise HTTPException(status_code=403, detail="School not verified")


@router.post("/initiate", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def initiate_payment(payment: PaymentInitiate, db: Session = Depends(get_db)):
    if payment.scholarship_id:
        scholarship = db.query(Scholarship).filter(Scholarship.id == payment.scholarship_id).first()
        if scholarship:
            await _check_school_verified(db, scholarship)

    provider = payment.payment_provider.lower() if payment.payment_provider else "paystack"
    reference = None

    if provider == "paystack":
        result = await paystack_service.initiate_payment(
            amount=float(payment.amount),
            email=payment.donor_email or "donor@example.com",
            metadata={"payment_type": "scholarship", "scholarship_id": payment.scholarship_id}
        )
        reference = result.get("data", {}).get("reference")
    elif provider == "flutterwave":
        result = await flutterwave_service.initiate_payment(
            amount=float(payment.amount),
            email=payment.donor_email or "donor@example.com",
            metadata={"payment_type": "scholarship", "scholarship_id": payment.scholarship_id}
        )
        reference = result.get("data", {}).get("tx_ref")
    elif provider == "interac":
        result = await interac_service.initiate_transfer(
            amount=float(payment.amount),
            email=payment.donor_email or "donor@example.com",
            metadata={"payment_type": "scholarship", "scholarship_id": payment.scholarship_id}
        )
        reference = result.get("transfer_id") or result.get("id") or str(payment.scholarship_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid payment provider")

    new_payment = Payment(
        scholarship_id=payment.scholarship_id,
        donor_email=payment.donor_email,
        amount=payment.amount,
        currency=payment.currency or "USD",
        payment_provider=provider,
        provider_reference=reference,
        status="pending"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("", response_model=List[PaymentResponse])
def list_payments(
    skip: int = 0,
    limit: int = 100,
    scholarship_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Payment)
    if scholarship_id:
        query = query.filter(Payment.scholarship_id == scholarship_id)
    if status:
        query = query.filter(Payment.status == status)
    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    return payments


@router.post("/verify/{reference}", response_model=PaymentVerifyResponse)
async def verify_payment(reference: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.provider_reference == reference).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    provider = payment.payment_provider.lower()

    if provider == "paystack":
        result = await paystack_service.verify_payment(reference)
        verified = result.get("data", {}).get("status") == "success"
    elif provider == "flutterwave":
        result = await flutterwave_service.verify_payment(reference)
        verified = result.get("data", {}).get("status") == "successful"
    else:
        raise HTTPException(status_code=400, detail="Invalid payment provider")

    if verified:
        payment.status = "verified"
        payment.verified_at = datetime.utcnow()
        db.commit()
        db.refresh(payment)

        if payment.scholarship_id:
            scholarship = db.query(Scholarship).filter(Scholarship.id == payment.scholarship_id).first()
            if scholarship:
                total_paid = sum(p.amount for p in scholarship.payments if p.status == "verified")
                if total_paid >= scholarship.total_amount:
                    scholarship.status = "fully_funded"
                elif total_paid > 0:
                    scholarship.status = "partially_funded"
                db.commit()

    return PaymentVerifyResponse(
        status=payment.status,
        amount=payment.amount,
        currency=payment.currency,
        provider_reference=payment.provider_reference
    )


@router.post("/receipt/{payment_id}")
async def generate_receipt(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.status != "verified":
        raise HTTPException(status_code=400, detail="Payment not verified")

    scholarship = None
    student_name = "Unknown"
    if payment.scholarship_id:
        scholarship = db.query(Scholarship).filter(Scholarship.id == payment.scholarship_id).first()
        if scholarship:
            student = db.query(Student).filter(Student.id == scholarship.student_id).first()
            if student:
                student_name = student.name

    pdf_bytes = receipt_service.generate_receipt(
        donor_name=payment.donor_email or "Anonymous",
        donor_email=payment.donor_email or "N/A",
        amount=float(payment.amount),
        currency=payment.currency,
        payment_reference=payment.provider_reference or str(payment.id),
        payment_date=payment.verified_at or payment.created_at,
        scholarship_details=scholarship.items if scholarship else [],
        student_name=student_name
    )

    return {
        "receipt": pdf_bytes.hex(),
        "content_type": "application/pdf"
    }


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return None