import httpx
import hashlib
import hmac
from typing import Optional, Dict, Any
from app.config import settings


class PaystackService:
    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.public_key = settings.PAYSTACK_PUBLIC_KEY
        self.webhook_secret = settings.PAYSTACK_WEBHOOK_SECRET
        self.base_url = "https://api.paystack.co"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    async def initiate_payment(
        self,
        amount: float,
        email: str,
        metadata: Optional[Dict[str, Any]] = None,
        currency: str = "USD"
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            payload = {
                "email": email,
                "amount": int(amount * 100),
                "currency": currency,
            }
            if metadata:
                payload["metadata"] = metadata

            response = await client.post(
                f"{self.base_url}/transaction/initialize",
                json=payload,
                headers=self._get_headers()
            )
            return response.json()

    async def verify_payment(self, reference: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/transaction/verify/{reference}",
                headers=self._get_headers()
            )
            return response.json()

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        if not self.webhook_secret:
            return False
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha512
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        event = payload.get("event")
        data = payload.get("data", {})

        result = {
            "event": event,
            "reference": data.get("reference"),
            "amount": data.get("amount"),
            "status": data.get("status"),
            "customer_email": data.get("customer", {}).get("email"),
            "metadata": data.get("metadata")
        }

        return result


paystack_service = PaystackService()