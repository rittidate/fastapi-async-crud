import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# import uuid
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import get_db, Base


SQLITE_DATABASE_TEST_URL = "sqlite+aiosqlite:///./test_db.db"

engine = create_async_engine(SQLITE_DATABASE_TEST_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://0.0.0.0") as client:
        yield client


@pytest.fixture()
def not_found_item_id():
    return 111
