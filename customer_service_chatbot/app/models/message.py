from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    sender: str  # 'user' or 'bot'
    content: str
    timestamp: datetime  # ✅ Use `datetime` instead of `str` for better validation