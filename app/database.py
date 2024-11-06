from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./items.db"

engine = create_async_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine)
Base = declarative_base()


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
