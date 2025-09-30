# tests/test_main.py

import pytest
from httpx import AsyncClient, ASGITransport # <--- IMPORTANTE: Importar o ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from main import app, get_db
from models import Base
from tests.test_database import TestingSessionLocal, engine


# Sobrescreve a dependência get_db para usar o banco de dados de teste
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db

# Fixture para garantir que o banco de dados é criado e limpo a cada teste
@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Fixture para criar um cliente de teste assíncrono (CORRIGIDO)
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    # AQUI ESTÁ A CORREÇÃO: Usamos o ASGITransport como "adaptador"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# --- Testes (não precisam de mudança) ---

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

@pytest.mark.asyncio
async def test_criar_usuario_sucesso(client: AsyncClient):
    response = await client.post(
        "/usuarios/",
        json={"email": "teste@exemplo.com", "senha": "senha123"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == "teste@exemplo.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_criar_usuario_email_duplicado(client: AsyncClient):
    await client.post("/usuarios/", json={"email": "duplicado@exemplo.com", "senha": "senha123"})
    response = await client.post(
        "/usuarios/",
        json={"email": "duplicado@exemplo.com", "senha": "outrasenha"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email já registado"}

@pytest.mark.asyncio
async def test_login_sucesso(client: AsyncClient):
    await client.post("/usuarios/", json={"email": "login@exemplo.com", "senha": "senha_correta"})
    response = await client.post(
        "/login",
        data={"username": "login@exemplo.com", "password": "senha_correta"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_senha_incorreta(client: AsyncClient):
    await client.post("/usuarios/", json={"email": "loginfalhou@exemplo.com", "senha": "senha_correta"})
    response = await client.post(
        "/login",
        data={"username": "loginfalhou@exemplo.com", "password": "senha_errada"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Email ou senha incorretos"}