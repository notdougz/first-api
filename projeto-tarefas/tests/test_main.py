import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from main import app, get_db
from models import Base
from tests.test_database import TestingSessionLocal, engine


# 1. Sobrescrever a dependência get_db para usar o banco de dados de teste
async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db

# 2. Pytest fixture para criar e destruir as tabelas para cada teste
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        # Usamos a Base importada de models para criar as tabelas corretas
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# 3. Pytest fixture para criar um cliente de teste
@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# 4. O nosso primeiro teste!
@pytest.mark.anyio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}