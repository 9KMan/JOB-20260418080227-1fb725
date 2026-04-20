import httpx
from typing import Optional, Dict, Any
from app.config import settings


class InteracService:
    def __init__(self):
        self.api_key = settings.INTERAC_API_KEY
        self.base_url = "https://api.interac.ca"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def initiate_transfer(
        self,
        amount: float,
        email: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            payload = {
                "amount": str(amount),
                "recipientEmail": email,
                "notificationLanguage": "en",
            }
            if metadata:
                payload["metadata"] = metadata

            response = await client.post(
                f"{self.base_url}/api/v2/selfserve/e-transfer/send",
                json=payload,
                headers=self._get_headers()
            )
            return response.json()

    async def verify_transfer(self, transfer_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v2/selfserve/e-transfer/{transfer_id}/status",
                headers=self._get_headers()
            )
            return response.json()

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        transfer_id = payload.get("transferId")
        status = payload.get("status")

        result = {
            "transfer_id": transfer_id,
            "status": status,
            "amount": payload.get("amount"),
            "recipient_email": payload.get("recipientEmail")
        }

        return result


interac_service = InteracService()