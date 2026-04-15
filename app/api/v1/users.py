from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user import user_service

router = APIRouter()

@router.post('/register',response_model=UserRead)
async def register(user_in:UserCreate, db:AsyncSession = Depends(get_db)):
    return await user_service.register_user(db,user_in=user_in)