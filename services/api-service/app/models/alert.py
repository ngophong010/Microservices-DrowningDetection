from beanie import Document, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

class Alert(Document):
    # Beanie will automatically create a MongoDB ObjectId for the primary key
    
    # Index the camera_id because we will frequently search for alerts by camera.
    camera_id: Indexed(str)
    
    # Index the timestamp for sorting and time-based queries.
    timestamp: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    
    confidence: float
    video_clip_url: Optional[str] = None
    # You could add a status field here later, e.g., status: str = "new"

    class Settings:
        name = "alerts"