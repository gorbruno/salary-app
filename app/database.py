from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.settings import settings
from app.models import Base

DATABASE = (
    f"sqlite+aiosqlite:///{settings.DB_NAME}.db"
)

engine = create_async_engine(DATABASE, echo=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"Database '{settings.DB_NAME}' initialized")

async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print(f"All tables from '{settings.DB_NAME}' database removed")

async def recreate_db():
    await drop_all_tables()
    await init_db()    

# декоратор для удобного обращения к базе
def connection(method):
    AsyncSessionLocal = async_sessionmaker[AsyncSession](
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False
    )
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper