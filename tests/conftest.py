import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.db.database import engine, Base, get_db, AsyncSessionLocal


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def override_get_db():
    async def _override_get_db():
        async with AsyncSessionLocal() as session:
            yield session
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()