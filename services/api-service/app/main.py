from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.db.session import init_db
from app.core.config import settings
from app.core.worker import CameraAnalysisWorker

from app.api.v1.endpoints import cameras, login

worker_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global worker_task
    await init_db()

    # Create an instance of the worker, explicitly passing the settings
    worker = CameraAnalysisWorker(settings=settings)

    # Create the background task for the worker's run method
    worker_task = asyncio.create_task(worker.run())

    yield
    
    # On shutdown, you can add cleanup logic here
    print("Application is shutting down. Cancelling worker task.")
    if worker_task:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            print("Worker task was cancelled successfully.")

app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME)

# Include the router from the cameras endpoint file
app.include_router(cameras.router, prefix="/api/v1/cameras", tags=["cameras"])
app.include_router(login.router, prefix="/api/v1", tags=["login"])
