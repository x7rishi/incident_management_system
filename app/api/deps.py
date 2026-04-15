from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.config import settings
from app.db.session import get_db
from app.repositories.user import user_repo
from app.models.user import User
from app.schemas.token import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        print(email)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        print('ffff')
        raise credentials_exception

    user = await user_repo.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
