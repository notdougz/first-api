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

# Fixture para criar um cliente de teste assíncrono
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- Testes Gerais ---

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

# --- Testes de Autenticação e Utilizador ---

@pytest.mark.asyncio
async def test_criar_usuario_sucesso(client: AsyncClient):
    response = await client.post(
        "/usuarios/",
        json={"email": "teste@exemplo.com", "senha": "senha123"},
    )
    data = response.json()
    # CORREÇÃO: O status code para criação é 201
    assert response.status_code == 201
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
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Email ou senha incorretos"}

@pytest.mark.asyncio
async def test_criar_e_listar_tarefas_autenticado(client: AsyncClient):
    # 1. Criar e fazer login do utilizador
    await client.post("/usuarios/", json={"email": "usertarefa@exemplo.com", "senha": "senha123"})
    login_response = await client.post(
        "/login",
        data={"username": "usertarefa@exemplo.com", "password": "senha123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Tentar listar tarefas (deve estar vazio)
    response_lista_vazia = await client.get("/tarefas/", headers=headers)
    assert response_lista_vazia.status_code == 200
    assert response_lista_vazia.json() == []

    # 3. Criar uma nova tarefa
    tarefa_data = {"titulo": "Minha primeira tarefa", "descricao": "Descrição da tarefa"}
    response_criacao = await client.post("/tarefas/", json=tarefa_data, headers=headers)
    assert response_criacao.status_code == 201
    data_criada = response_criacao.json()
    assert data_criada["titulo"] == tarefa_data["titulo"]
    assert "id" in data_criada

    # 4. Listar tarefas novamente (deve conter a tarefa criada)
    response_lista_cheia = await client.get("/tarefas/", headers=headers)
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
    # Criar Utilizador A e sua tarefa
    await client.post("/usuarios/", json={"email": "userA@exemplo.com", "senha": "123"})
    login_a = await client.post("/login", data={"username": "userA@exemplo.com", "password": "123"})
    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    response_tarefa_a = await client.post("/tarefas/", json={"titulo": "Tarefa do User A"}, headers=headers_a)
    tarefa_a_id = response_tarefa_a.json()["id"]

    # Criar Utilizador B e fazer login
    await client.post("/usuarios/", json={"email": "userB@exemplo.com", "senha": "456"})
    login_b = await client.post("/login", data={"username": "userB@exemplo.com", "password": "456"})
    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Utilizador B tenta aceder à tarefa do Utilizador A
    response_b_get = await client.get(f"/tarefas/{tarefa_a_id}", headers=headers_b)
    # A API corretamente retorna 403 Forbidden
    assert response_b_get.status_code == 403
    
@pytest.mark.asyncio
async def test_atualizar_tarefa_sucesso(client: AsyncClient):
    # 1. Criar usuário e fazer login
    await client.post("/usuarios/", json={"email": "user_update@exemplo.com", "senha": "123"})
    login_res = await client.post("/login", data={"username": "user_update@exemplo.com", "password": "123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar a tarefa que será atualizada
    tarefa_original = {"titulo": "Título Antigo", "descricao": "Descrição Antiga"}
    criar_res = await client.post("/tarefas/", json=tarefa_original, headers=headers)
    tarefa_id = criar_res.json()["id"]
    
    # 3. Atualizar a tarefa
    dados_atualizados = {"titulo": "Título Novo!", "descricao": "Descrição Nova!", "concluida": True}
    update_res = await client.put(f"/tarefas/{tarefa_id}", json=dados_atualizados, headers=headers)
    
    # 4. Verificar a resposta imediata da atualização
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["titulo"] == "Título Novo!"
    assert data["concluida"] is True

    # 5. Buscar a tarefa novamente no banco para garantir que a mudança foi salva
    response_get_depois = await client.get(f"/tarefas/{tarefa_id}", headers=headers)
    assert response_get_depois.status_code == 200
    dados_do_banco = response_get_depois.json()
    assert dados_do_banco["titulo"] == "Título Novo!"
    assert dados_do_banco["descricao"] == "Descrição Nova!"
    assert dados_do_banco["concluida"] is True
    
@pytest.mark.asyncio
async def test_deletar_tarefa_sucesso(client: AsyncClient):
    # 1. Criar usuário e fazer login
    await client.post("/usuarios/", json={"email": "user_delete@exemplo.com", "senha": "123"})
    login_res = await client.post("/login", data={"username": "user_delete@exemplo.com", "password": "123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar a tarefa
    tarefa_data = {"titulo": "Tarefa para deletar"}
    criar_res = await client.post("/tarefas/", json=tarefa_data, headers=headers)
    tarefa_id = criar_res.json()["id"]

    # 3. Deletar a tarefa
    delete_res = await client.delete(f"/tarefas/{tarefa_id}", headers=headers)
    assert delete_res.status_code == 200

    # 4. Verificar se a tarefa não existe mais (deve retornar 404)
    get_res = await client.get(f"/tarefas/{tarefa_id}", headers=headers)
    assert get_res.status_code == 404
    
@pytest.mark.asyncio
async def test_error_ao_atualizar_tarefa_de_outro_usuario(client: AsyncClient):
    # Criar Utilizador A e sua tarefa
    await client.post("/usuarios/", json={"email": "userA_err@exemplo.com", "senha": "123"})
    login_a = await client.post("/login", data={"username": "userA_err@exemplo.com", "password": "123"})
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}
    tarefa_a_res = await client.post("/tarefas/", json={"titulo": "Tarefa do User A"}, headers=headers_a)
    tarefa_a_id = tarefa_a_res.json()["id"]

    # Criar Utilizador B
    await client.post("/usuarios/", json={"email": "userB_err@exemplo.com", "senha": "456"})
    login_b = await client.post("/login", data={"username": "userB_err@exemplo.com", "password": "456"})
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    # Utilizador B tenta atualizar a tarefa do Utilizador A
    response_put = await client.put(f"/tarefas/{tarefa_a_id}", json={"titulo": "invadido"}, headers=headers_b)
    assert response_put.status_code == 403

@pytest.mark.asyncio
async def test_acoes_em_tarefa_inexistente_retorna_404(client: AsyncClient):
    # 1. Fazer login para ter um token válido
    await client.post("/usuarios/", json={"email": "user_404@exemplo.com", "senha": "123"})
    login_res = await client.post("/login", data={"username": "user_404@exemplo.com", "password": "123"})
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}
    
    id_inexistente = 99999

    # 2. Tentar obter, atualizar e deletar uma tarefa que não existe
    response_get = await client.get(f"/tarefas/{id_inexistente}", headers=headers)
    assert response_get.status_code == 404

    response_put = await client.put(f"/tarefas/{id_inexistente}", json={"titulo": "novo"}, headers=headers)
    assert response_put.status_code == 404

    response_delete = await client.delete(f"/tarefas/{id_inexistente}", headers=headers)
    assert response_delete.status_code == 404
    
@pytest.mark.asyncio
async def test_error_ao_deletar_tarefa_de_outro_usuario(client: AsyncClient):
    # Criar Utilizador A e sua tarefa
    await client.post("/usuarios/", json={"email": "userA_del_err@exemplo.com", "senha": "123"})
    login_a = await client.post("/login", data={"username": "userA_del_err@exemplo.com", "password": "123"})
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}
    tarefa_a_res = await client.post("/tarefas/", json={"titulo": "Tarefa do User A"}, headers=headers_a)
    tarefa_a_id = tarefa_a_res.json()["id"]

    # Criar Utilizador B
    await client.post("/usuarios/", json={"email": "userB_del_err@exemplo.com", "senha": "456"})
    login_b = await client.post("/login", data={"username": "userB_del_err@exemplo.com", "password": "456"})
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    # Utilizador B tenta deletar a tarefa do Utilizador A
    response_delete = await client.delete(f"/tarefas/{tarefa_a_id}", headers=headers_b)
    assert response_delete.status_code == 403