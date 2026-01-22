from typing import AsyncGenerator

import pytest
import pytest_asyncio
import starlette.status
from api.db import Base, get_db
from api.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async_engine = create_async_engine(
        ASYNC_DB_URL,
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        await async_engine.dispose()


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post("/tasks", json={"title": "テストタスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク"

    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "テストタスク"
    assert response_obj[0]["done"] is False


@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "テストタスク2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク2"

    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_param, expectation",
    [
        ("2024-12-01", starlette.status.HTTP_200_OK),
        ("2024-12-32", starlette.status.HTTP_422_UNPROCESSABLE_CONTENT),
        ("2024/12/01", starlette.status.HTTP_422_UNPROCESSABLE_CONTENT),
        ("2024-1201", starlette.status.HTTP_422_UNPROCESSABLE_CONTENT),
    ],
)
async def test_due_date(input_param, expectation, async_client):
    response = await async_client.post(
        "/tasks", json={"title": "テストタスク", "due_date": input_param}
    )
    assert response.status_code == expectation
