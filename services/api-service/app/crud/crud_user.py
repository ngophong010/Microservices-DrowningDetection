from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get(id: str) -> User | None:
    """Get a single user by their ID."""
    return await User.get(id)

async def get_by_email(email: str) -> User | None:
    return await User.find_one(User.email == email)

async def create(user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)
    await user.insert()
    return user
