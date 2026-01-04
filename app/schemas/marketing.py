from datetime import datetime
from pydantic import BaseModel


class MarketingMessage(BaseModel):
    subject: str
    body_html: str
    received_at: datetime