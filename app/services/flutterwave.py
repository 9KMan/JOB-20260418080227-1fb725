import httpx
from typing import Optional, Dict, Any
from app.config import settings


class FlutterwaveService:
    def __init__(self):
        self.secret_key = settings.FLUTTERWAVE_SECRET_KEY
        self.public_key = settings.FLUTTERWAVE_PUBLIC_KEY
        self.webhook_secret = settings.FLUTTERWAVE_WEBHOOK_SECRET
        self.base_url = "https://api.flutterwave.com/v3"

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
                "tx_ref": f"tx_{metadata.get('scholarship_id', 'unknown')}_{int(amount * 100)}",
                "amount": str(amount),
                "currency": currency,
                "email": email,
                "customer": {
                    "email": email
                }
            }
            if metadata:
                payload["meta"] = metadata

            response = await client.post(
                f"{self.base_url}/payments",
                json=payload,
                headers=self._get_headers()
            )
            return response.json()

    async def verify_payment(self, tx_ref: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/transactions/{tx_ref}/verify",
                headers=self._get_headers()
            )
            return response.json()

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        if not self.webhook_secret:
            return False
        import hashlib
        expected_signature = hashlib.sha256(
            payload + self.webhook_secret.encode()
        ).hexdigest()
        return expected_signature == signature

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        event = payload.get("event")
        data = payload.get("data", {})

        result = {
            "event": event,
            "tx_ref": data.get("tx_ref"),
            "amount": data.get("amount"),
            "status": data.get("status"),
            "customer_email": data.get("customer", {}).get("email"),
            "metadata": data.get("meta")
        }

        return result


flutterwave_service = FlutterwaveService()