import asyncio
import httpx
from app.crud import crud_camera, crud_alert
from app.core.config import Settings

class CameraAnalysisWorker:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.run_interval_seconds = 10 # How often the loop runs

    async def run(self):
        """The main worker loop that runs indefinitely."""
        print("Starting camera analysis worker...")
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    active_cameras = await crud_camera.get_multi_active()
                    if active_cameras:
                        print(f"Worker found {len(active_cameras)} active cameras to analyze.")

                    for cam in active_cameras:
                        # Construct the URL for the ai-service using the Docker DNS name
                        analysis_url = "http://ai-service:8001/analyze"
                        
                        response = await client.post(analysis_url, json={
                            "camera_id": cam.id,
                            "stream_url": cam.stream_url
                        }, timeout=30.0)
                        
                        response.raise_for_status()
                        result = response.json()
                        
                        if result.get("drowning_detected"):
                            print(f"Worker creating alert for camera {cam.id}")
                            await crud_alert.create(
                                camera_id=cam.id,
                                confidence=result.get("confidence", 0.0)
                            )
                
                except httpx.RequestError as e:
                    print(f"An error occurred while requesting analysis: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred in the worker: {e}")

                await asyncio.sleep(self.run_interval_seconds)
