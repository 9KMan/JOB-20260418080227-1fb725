from typing import Dict, Any
from app.config import settings


class NotificationService:
    def __init__(self):
        self.sendgrid_api_key = settings.SENDGRID_API_KEY
        self.twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    def notify_payment_received(
        self,
        db,
        user_type: str,
        user_id: int,
        donor_email: str,
        amount: float,
        currency: str
    ):
        from app.models import Notification
        message = f"Payment received from {donor_email}: {currency} {amount}"

        notification = Notification(
            user_type=user_type,
            user_id=user_id,
            notification_type="payment_received",
            message=message
        )
        db.add(notification)
        db.commit()

        self._send_email(
            to_email=donor_email,
            subject="Thank you for your donation",
            body=f"Your payment of {currency} {amount} has been received. Thank you for supporting our scholarship program!"
        )

        return notification

    def notify_deadline(
        self,
        db,
        user_type: str,
        user_id: int,
        deadline_message: str
    ):
        from app.models import Notification
        notification = Notification(
            user_type=user_type,
            user_id=user_id,
            notification_type="deadline",
            message=deadline_message
        )
        db.add(notification)
        db.commit()
        return notification

    def _send_email(self, to_email: str, subject: str, body: str):
        if not self.sendgrid_api_key:
            return {"status": "disabled", "message": "SendGrid not configured"}

        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            message = Mail(
                from_email="noreply@scholarshipplatform.com",
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )

            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            return {"status": "sent", "code": response.status_code}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _send_sms(self, to_phone: str, message: str):
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            return {"status": "disabled", "message": "Twilio not configured"}

        try:
            from twilio.rest import Client

            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=to_phone
            )
            return {"status": "sent", "sid": message.sid}
        except Exception as e:
            return {"status": "error", "message": str(e)}


notification_service = NotificationService()