import pytest
from app.database import init_db, drop_all_tables, engine
from sqlalchemy import text

### тест бд ###
@pytest.mark.asyncio
async def test_db_creation_and_deletion():
    # создание
    await init_db()
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
    assert len(tables) > 0

    # удаление
    await drop_all_tables()
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
    assert len(tables) == 0