from typing import List
from app.models.camera import Camera
from app.schemas.camera import CameraCreate

class CRUDCamera:
    async def create(camera_in: CameraCreate) -> Camera:
        camera = Camera(**camera_in.model_dump())
        await camera.insert()
        return camera

    async def get(id: str) -> Camera | None:
        return await Camera.get(id)

    async def get_multi() -> List[Camera]:
        return await Camera.find_all().to_list()

    async def get_multi_active(self) -> List[Camera]:
        """Get all cameras that are currently marked as active."""
        return await Camera.find(Camera.is_active == True).to_list()

camera = CRUDCamera()