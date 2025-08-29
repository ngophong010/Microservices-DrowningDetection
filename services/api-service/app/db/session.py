import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.camera import Camera # We will create this next
# Import other models like Alert here as you create them
from app.models.user import User
from app.models.alert import Alert

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client.get_database(settings.DATABASE_NAME),
        document_models=[
            Camera,
            Alert,
            User
            ] # Add Alert, User etc. here
    )
    print("Database initialized.")
