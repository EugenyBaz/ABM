import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.api.deps import get_db
from app.core.config import settings
from app.main import app

DATABASE_URL = settings.DATABASE_URL


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


# ---------- DB session ----------


@pytest_asyncio.fixture
async def db_session(engine):
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session


# ---------- Override get_db ----------
@pytest_asyncio.fixture
async def override_get_db(db_session):
    async def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


# ---------- Clean DB ----------
@pytest_asyncio.fixture(autouse=True)
async def clean_db(override_get_db, db_session):
    await db_session.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE"))
    await db_session.commit()


# ---------- HTTP client ----------
@pytest_asyncio.fixture
async def client(override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


# ---------- Headers ----------
@pytest.fixture
def user_1_headers():
    return {"x-telegram-user-id": "111"}


@pytest.fixture
def user_2_headers():
    return {"x-telegram-user-id": "222"}
