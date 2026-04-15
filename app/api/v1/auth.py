from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.services.auth import auth_service
from app.schemas.token import Token 
from typing import Annotated

router = APIRouter()

@router.post('/login', response_model=Token)
async def login_for_access_token(
    db: Annotated[AsyncSession, Depends(get_db)], 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await auth_service.authenticate(
        db, email=form_data.username, password = form_data.password 
    )
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}