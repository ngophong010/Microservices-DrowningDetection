from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CameraBase(BaseModel):
    name: str
    stream_url: str
    is_active: bool = True
    location: Optional[str] = None

class CameraCreate(CameraBase):
    pass

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    stream_url: Optional[str] = None
    is_active: Optional[bool] = None
    location: Optional[str] = None

class CameraInDB(CameraBase):
    id: str = Field(alias="_id")
    created_at: datetime

    class Config:
        orm_mode = True # This allows mapping from the DB model
