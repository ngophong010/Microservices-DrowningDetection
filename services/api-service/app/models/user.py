from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional
import uuid

class User(Document):
    id: str = Field(default_factory=lambda: f"user_{uuid.uuid4().hex[:6]}", alias="_id")
    email: Indexed(EmailStr, unique=True) # Emails must be unique
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    class Settings:
        name = "users"
