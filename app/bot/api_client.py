import httpx
from app.core.config import settings

class BackendClient:
    def __init__(self):
        self.base_url = settings.API_URL

    async def create_task(self, user_id: int, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tasks/",
                json=data,
                headers={"X-Telegram-User-Id": str(user_id)},
                timeout=5,
            )
            response.raise_for_status()
            return response.json()