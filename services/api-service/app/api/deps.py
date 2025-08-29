from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.core import security
from app.core.config import settings
from app.models.user import User
from app import crud

# This tells FastAPI where to go to get a token.
# The client will call /api/v1/token to get a token, then it will send that
# token in the Authorization header for every protected request.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/token"
)

async def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    try:
        # Decode the token to get the payload
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # The "sub" (subject) of the token is the user's ID
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials (no user id in token)",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials (invalid token)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Use the ID from the token to fetch the user from the database
    user = await crud.crud_user.get(id=user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user
