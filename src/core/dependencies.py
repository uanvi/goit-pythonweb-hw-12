from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.auth import verify_token
from src.core.cache import get_cached_user, cache_user
from src.crud.user import get_user_by_email
from src.models.user import User

security = HTTPBearer()

def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token with Redis caching.
    
    Args:
        token: JWT bearer token
        db: Database session
        
    Returns:
        Authenticated user object
        
    Raises:
        HTTPException: If token invalid or user not found
    """
    # Get token from Bearer schema
    credentials = token.credentials
    email = verify_token(credentials)
    
    # First try to get user from database to get user_id
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Try to get user from cache
    cached_data = get_cached_user(user.id)
    if cached_data:
        # Return user-like object from cache
        user.username = cached_data["username"]
        user.is_verified = cached_data["is_verified"]
        user.avatar_url = cached_data["avatar_url"]
        return user
    
    # Cache user for next requests
    cache_user(user)
    
    return user