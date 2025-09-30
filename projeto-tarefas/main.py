import pytest
from httpx import AsyncClient, ASGITransport
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

# Fixture para criar um cliente de teste anónimo
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- NOVA FIXTURE PARA UM CLIENTE AUTENTICADO ---
@pytest.fixture
async def authenticated_client(client: AsyncClient) -> AsyncClient:
    """
    Cria um utilizador, faz login e devolve o cliente com o header de autorização já configurado.
    """
    await client.post("/usuarios/", json={"email": "authuser@exemplo.com", "senha": "senha123"})
    login_response = await client.post(
        "/login",
        data={"username": "authuser@exemplo.com", "password": "senha123"},
    )
    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client

# --- Testes ---

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

# (Os testes de login e registo continuam iguais, usando o 'client' anónimo)
@pytest.mark.asyncio
async def test_criar_usuario_sucesso(client: AsyncClient):
    response = await client.post("/usuarios/",json={"email": "teste@exemplo.com", "senha": "senha123"})
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == "teste@exemplo.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_criar_usuario_email_duplicado(client: AsyncClient):
    await client.post("/usuarios/", json={"email": "duplicado@exemplo.com", "senha": "senha123"})
    response = await client.post("/usuarios/", json={"email": "duplicado@exemplo.com", "senha": "outrasenha"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email já registado"}

@pytest.mark.asyncio
async def test_login_sucesso(client: AsyncClient):
    await client.post("/usuarios/", json={"email": "login@exemplo.com", "senha": "senha_correta"})
    response = await client.post("/login", data={"username": "login@exemplo.com", "password": "senha_correta"})
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_senha_incorreta(client: AsyncClient):
    await client.post("/usuarios/", json={"email": "loginfalhou@exemplo.com", "senha": "senha_correta"})
    response = await client.post("/login", data={"username": "loginfalhou@exemplo.com", "password": "senha_errada"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Email ou senha incorretos"}

# --- TESTES DE TAREFAS (AGORA USANDO A NOVA FIXTURE) ---

@pytest.mark.asyncio
async def test_criar_e_listar_tarefas_autenticado(authenticated_client: AsyncClient):
    # 1. Tentar listar tarefas (deve estar vazio)
    response_lista_vazia = await authenticated_client.get("/tarefas/")
    assert response_lista_vazia.status_code == 200
    assert response_lista_vazia.json() == []

    # 2. Criar uma nova tarefa
    tarefa_data = {"titulo": "Minha tarefa autenticada", "descricao": "Descrição"}
    response_criacao = await authenticated_client.post("/tarefas/", json=tarefa_data)
    assert response_criacao.status_code == 201
    data_criada = response_criacao.json()
    assert data_criada["titulo"] == tarefa_data["titulo"]

    # 3. Listar tarefas novamente (deve conter a tarefa criada)
    response_lista_cheia = await authenticated_client.get("/tarefas/")
    assert response_lista_cheia.status_code == 200
    lista_tarefas = response_lista_cheia.json()
    assert len(lista_tarefas) == 1
    assert lista_tarefas[0]["titulo"] == tarefa_data["titulo"]

@pytest.mark.asyncio
async def test_acesso_negado_tarefas_sem_token(client: AsyncClient):
    response = await client.get("/tarefas/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

@pytest.mark.asyncio
async def test_utilizador_nao_pode_ver_tarefa_de_outro(client: AsyncClient):
    # Criar Utilizador A e a sua tarefa
    await client.post("/usuarios/", json={"email": "userA@exemplo.com", "senha": "123"})
    login_a = await client.post("/login", data={"username": "userA@exemplo.com", "password": "123"})
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}
    response_tarefa_a = await client.post("/tarefas/", json={"titulo": "Tarefa do User A"}, headers=headers_a)
    tarefa_a_id = response_tarefa_a.json()["id"]

    # Criar Utilizador B
    await client.post("/usuarios/", json={"email": "userB@exemplo.com", "senha": "456"})
    login_b = await client.post("/login", data={"username": "userB@exemplo.com", "password": "456"})
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}
    
    # Utilizador B tenta aceder à tarefa do Utilizador A e falha
    response_b_get = await client.get(f"/tarefas/{tarefa_a_id}", headers=headers_b)
    assert response_b_get.status_code == 404