from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import user_repo
from app.core.security import verify_password

class AuthService: 
    async def authenticate(
            self, db: AsyncSession, email: str, password: str
    ):
        user = await user_repo.get_by_email(db, email=email)
        if not user: 
            return None 
        if not verify_password(password, user.hashed_password):
            return None 
        return user 
    

auth_service = AuthService()