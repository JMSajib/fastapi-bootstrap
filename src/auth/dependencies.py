from fastapi import Depends, HTTPException, status
from src.auth.routes import get_current_user


async def is_admin(user: dict = Depends(get_current_user)):
    if not user or user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication Failed. You do not have admin permissions.',
        )
    return user
