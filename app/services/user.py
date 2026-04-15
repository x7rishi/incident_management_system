from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 
from app.repositories.user import user_repo
from app.schemas.user import UserCreate
from app.core.security import get_password_has

class UserService:
    async def register_user(self,db:AsyncSession, user_in: UserCreate):
        user_exists = await user_repo.get_by_email(db,email=user_in.email)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='A user with this email Id already exists.'
            )
        
        hashed_password = get_password_has(user_in.password)
        user_data = user_in.model_dump(exclude={"password"})
        user_data['hashed_password'] = hashed_password


        from app.models.user import User
        db_obj = User(**user_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    

user_service = UserService()