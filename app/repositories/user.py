from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.user import User 


class UserRepository(BaseRepository[User]):
    async def get_by_email(self,db:AsyncSession,email:str)-> User | None:
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    


user_repo = UserRepository(User)