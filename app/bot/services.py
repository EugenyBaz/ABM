import aiohttp
from typing import List, Dict

API_URL = "http://127.0.0.1:8000/tasks/"

async def create_task_api(title: str, description: str, user_id: int):
    payload = {"title": title, "description": description}
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as resp:
            return await resp.json()