from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import Payment, Scholarship
from app.services.paystack import paystack_service
from app.services.flutterwave import flutterwave_service
from app.services.notification import notification_service

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/paystack")
async def paystack_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_paystack_signature: Optional[str] = Header(None)
):
    payload = await request.body()

    if x_paystack_signature:
        if not paystack_service.verify_webhook_signature(payload, x_paystack_signature):
            raise HTTPException(status_code=400, detail="Invalid signature")

    data = await request.json()
    event = data.get("event")
    event_data = data.get("data", {})

    reference = event_data.get("reference")

    payment = db.query(Payment).filter(Payment.provider_reference == reference).first()

    if event == "transaction.success":
        if payment:
            payment.status = "verified"
            payment.verified_at = datetime.utcnow()
            db.commit()

            if payment.scholarship_id:
                scholarship = db.query(Scholarship).filter(Scholarship.id == payment.scholarship_id).first()
                if scholarship:
                    total_paid = sum(p.amount for p in scholarship.payments if p.status == "verified")
                    if total_paid >= scholarship.total_amount:
                        scholarship.status = "fully_funded"
                    elif total_paid > 0:
                        scholarship.status = "partially_funded"
                    db.commit()

                    notification_service.notify_payment_received(
                        db, "student", scholarship.student_id,
                        payment.donor_email, float(payment.amount), payment.currency
                    )

        return {"status": "success"}

    elif event == "transaction.failed":
        if payment:
            payment.status = "failed"
            db.commit()
        return {"status": "failed"}

    return {"status": "received"}


@router.post("/flutterwave")
async def flutterwave_webhook(
    request: Request,
    db: Session = Depends(get_db),
    http_auth: Optional[str] = Header(None)
):
    data = await request.json()
    event = data.get("event")
    event_data = data.get("data", {})

    tx_ref = event_data.get("tx_ref")

    payment = db.query(Payment).filter(Payment.provider_reference == tx_ref).first()

    if event == "charge.completed" or event_data.get("status") == "successful":
        if payment:
            payment.status = "verified"
            payment.verified_at = datetime.utcnow()
            db.commit()

            if payment.scholarship_id:
                scholarship = db.query(Scholarship).filter(Scholarship.id == payment.scholarship_id).first()
                if scholarship:
                    total_paid = sum(p.amount for p in scholarship.payments if p.status == "verified")
                    if total_paid >= scholarship.total_amount:
                        scholarship.status = "fully_funded"
                    elif total_paid > 0:
                        scholarship.status = "partially_funded"
                    db.commit()

                    notification_service.notify_payment_received(
                        db, "student", scholarship.student_id,
                        payment.donor_email, float(payment.amount), payment.currency
                    )

        return {"status": "success"}

    elif event in ["charge.failed", "charge.declined"]:
        if payment:
            payment.status = "failed"
            db.commit()
        return {"status": "failed"}

    return {"status": "received"}