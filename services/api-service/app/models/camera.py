from beanie import Document, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime
import uuid

class Camera(Document):
    id: str = Field(default_factory=lambda: f"cam_{uuid.uuid4().hex[:6]}", alias="_id")
    name: Indexed(str)
    stream_url: str
    is_active: bool = True
    location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "cameras"
