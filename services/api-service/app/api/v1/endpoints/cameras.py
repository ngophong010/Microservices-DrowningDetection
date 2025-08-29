from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app import crud
from app.api import deps
from app.crud import crud_camera
from app.schemas import camera as camera_schema
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=camera_schema.CameraInDB, status_code=status.HTTP_201_CREATED)
async def create_camera(
    camera_in: camera_schema.CameraCreate,
    # This is the dependency. FastAPI will run deps.get_current_user and inject
    # the result into the 'current_user' variable.
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new camera. Only accessible to authenticated users.
    """
    print(f"User {current_user.email} is creating a camera.")
    return await crud.crud_camera.create(camera_in)

@router.get("/", response_model=List[camera_schema.CameraInDB])
async def read_cameras(
    current_user: User = Depends(deps.get_current_user)
):
    
    return await crud_camera.get_multi()

@router.get("/{id}", response_model=camera_schema.CameraInDB)
async def read_camera(
    id: str,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retrieve a specific camera. Only accessible to authenticated users.
    """
    camera = await crud.crud_camera.get(id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera
