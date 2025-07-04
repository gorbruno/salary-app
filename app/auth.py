from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.settings import settings
from app.utils import get_user_by_id
from app.models import UserIdDTO, UserDTO
from typing import Optional
import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# jwt работает только со словарём
def create_access_token(data: UserIdDTO, expires: datetime.timedelta | None = None):
    to_encode = {"id": data.id}
    expire = datetime.datetime.now(datetime.timezone.utc) + (expires or datetime.timedelta(minutes=15))
    to_encode.update({"exp": expire}) #type: ignore
    token = jwt.encode(to_encode, settings.SECRET_TOKEN, algorithm=settings.ENCRYPTION_ALGORITHM)
    return token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[UserDTO]:
    try:
        payload = jwt.decode(token, settings.SECRET_TOKEN, algorithms=[settings.ENCRYPTION_ALGORITHM])
        user_id: Optional[int] = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user: Optional[UserDTO]  = await get_user_by_id(id=user_id) #type: ignore
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")