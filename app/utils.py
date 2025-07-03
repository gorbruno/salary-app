from app.database import connection
from sqlalchemy import select
from app.models import UserORM, UserDTO, UserIdDTO
from typing import Optional
from app.database import init_db, recreate_db
import csv
from datetime import datetime

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

async def create_database_with_mockup_data(
        data: str,
        drop_database: bool = True,
        date_format: str = "%m/%d/%y"
    ):
    if drop_database:
        await recreate_db()
    else:
        await init_db()
    try:
        with open(data, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for n, row in enumerate(reader, 1):
                try:
                    row['salary'] = int(row['salary'])
                    row['promotion_date'] = datetime.strptime(row['promotion_date'], date_format)
                    await add_user(**row)
                except Exception as e:
                    raise ImportError(f"Error in row {n} ({row}): {e}")
    except Exception as e:
        raise ImportError(f"Cannot create database from table {data}: {e}")
    print(f"Data from {data} added into the database")