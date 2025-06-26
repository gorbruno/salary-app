from app.database import connection
from sqlalchemy import select
from app.models import UserORM, UserDTO, UserIdDTO
from typing import Optional

@connection
async def get_id_by_credentials(username, password,  session) -> Optional[UserIdDTO]:
    result = await session.execute(
        select(UserORM)
        .where(UserORM.username == username, UserORM.password == password)
    )
    user_id: Optional[UserORM] = result.scalars().first()
    if user_id:
        return UserIdDTO.model_validate(user_id)
    else:
        return None

@connection
async def get_user_by_id(id, session) -> Optional[UserORM]:
    result = await session.execute(
        select(UserORM)
        .where(UserORM.id == id)
    )
    return result.scalars().first()

@connection
async def add_user(session, **kwargs)-> None:
    user_valid = UserDTO.model_validate(kwargs)
    new_user = UserORM(**user_valid.model_dump())
    session.add(new_user)
    await session.commit()