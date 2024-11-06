import pytest
import pytest_asyncio
import asyncio

# import uuid
from httpx import AsyncClient, ASGITransport
from app.database import DatabaseSessionManager, get_db_session
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_items.db"

sessionmanager = DatabaseSessionManager(TEST_DATABASE_URL, {"echo": True})


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def transactional_session():
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()  # Rolls back the outer transaction


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def get_db_session_override():
        yield db_session[0]

    app.dependency_overrides[get_db_session] = get_db_session_override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://0.0.0.0") as client:
        yield client


