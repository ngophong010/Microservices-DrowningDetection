from fastapi import FastAPI, status
from pydantic import BaseModel
import random # We'll use this to simulate detection for now

app = FastAPI(title="Drowning Detection AI Service")

class StreamAnalysisRequest(BaseModel):
    camera_id: str
    stream_url: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "AI Service is running"}

@app.post("/analyze")
def analyze_stream(request: StreamAnalysisRequest):
    """
    Receives a stream URL and performs AI analysis.
    In a real-world scenario, this is where you would use OpenCV to
    process the video stream and run it through your ML model.
    """
    print(f"Analyzing stream for camera: {request.camera_id} at {request.stream_url}")
    
    # --- MOCK AI LOGIC ---
    # Simulate a 10% chance of detecting a drowning event
    drowning_detected = random.random() < 0.1 
    confidence = 0.0
    if drowning_detected:
        confidence = round(random.uniform(0.85, 0.98), 2)
        print(f"!!! DROWNING DETECTED for camera {request.camera_id} with confidence {confidence} !!!")
    # --- END MOCK AI LOGIC ---
    
    return {
        "drowning_detected": drowning_detected,
        "confidence": confidence
    }
