from fastapi import FastAPI, status,  HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import time

# --- Data Models (using Pydantic) ---
class Camera(BaseModel):
    id: str = Field(default_factory=lambda: f"cam_{uuid.uuid4().hex[:6]}")
    name: str
    stream_url: str
    is_active: bool = True
    location: Optional[str] = None

# --- In-Memory "Database" (for now) ---
db = {
    "cameras": [
        Camera(id="cam_123", name="Main Pool Cam", stream_url="rtsp://fake/1", is_active=True, location="Main Pool"),
        Camera(id="cam_456", name="Kiddie Pool Cam", stream_url="rtsp://fake/2", is_active=False, location="Kiddie Pool"),
    ]
}

# Create an instance of the FastAPI class
app = FastAPI()

@app.get("/api/v1/cameras", response_model=List[Camera])
def get_cameras():
    return db["cameras"]

@app.post("/api/v1/cameras", response_model=Camera, status_code=status.HTTP_201_CREATED)
def create_camera(camera: Camera):
    db["cameras"].append(camera)
    return camera

@app.get("/api/v1/cameras/{camera_id}", response_model=Camera)
def get_camera_by_id(camera_id: str):
    for cam in db["cameras"]:
        if cam.id == camera_id:
            return cam
    raise HTTPException(status_code=404, detail="Camera not found")