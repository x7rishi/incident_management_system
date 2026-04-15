from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt 
from app.core.config import settings 


pwd = CryptContext(schemes=['bcrypt'],deprecated='auto')



def get_password_has(password: str) ->str:
    return pwd.hash(password)


def verify_password(password, hashed_password) -> bool:
    return pwd.verify(password, hashed_password)


def create_access_token(data:dict,expires_delta:timedelta | None ) ->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)