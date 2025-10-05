"""
Suíte de Testes de Integração para a API de Tarefas

Estes testes verificam o comportamento da aplicação FastAPI como um todo,
simulando requisições HTTP e validando as respostas contra um banco de
dados de teste isolado e em memória.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, NamedTuple

from main import app, get_db
from models import Base
from tests.test_database import TestingSessionLocal, engine

# --- Configuração Inicial dos Testes (Fixtures e Overrides) ---

@pytest.fixture(scope="session", autouse=True)
def override_database_dependency():
    """
    Fixture de sessão que substitui a dependência `get_db` da aplicação
    pela nossa sessão de banco de dados de teste (`TestingSessionLocal`).
    Garante que toda a suíte de testes use o banco de dados em memória.
    """
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with TestingSessionLocal() as db:
            yield db
    app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_and_teardown_db():
    """
    Fixture que é executada para cada teste (`autouse=True`).
    - Antes de cada teste: Cria todas as tabelas (schema) no banco de dados.
    - Depois de cada teste: Apaga todas as tabelas.
    Isto garante que cada teste comece com um banco de dados limpo e isolado.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture que cria e fornece um cliente HTTP assíncrono (httpx)
    para interagir com a aplicação FastAPI nos testes.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- Fixture Avançada para Autenticação ---

class AuthenticatedClient(NamedTuple):
    client: AsyncClient
    token: str
    headers: dict
    user_id: int
    email: str

@pytest.fixture
async def authenticated_client(client: AsyncClient) -> AuthenticatedClient:
    """
    Fixture reutilizável que cria um utilizador, faz login e retorna um
    cliente autenticado com o token, headers e ID do utilizador.
    Simplifica drasticamente os testes que requerem um utilizador logado.
    """
    email = "teste.auth@exemplo.com"
    password = "senha_segura_123"
    
    # Criar utilizador
    response = await client.post("/usuarios/", json={"email": email, "senha": password})
    user_id = response.json()["id"]

    # Fazer login
    login_response = await client.post("/login", data={"username": email, "password": password})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    return AuthenticatedClient(client=client, token=token, headers=headers, user_id=user_id, email=email)


# --- Suítes de Testes Agrupadas por Funcionalidade ---

class TestAuth:
    """Testes para o fluxo de registo e autenticação."""

    @pytest.mark.asyncio
    async def test_criar_usuario_sucesso(self, client: AsyncClient):
        """Verifica se um novo utilizador pode ser criado com sucesso."""
        # Arrange
        user_data = {"email": "novo@exemplo.com", "senha": "senha_valida_123"}

        # Act
        response = await client.post("/usuarios/", json=user_data)
        data = response.json()

        # Assert
        assert response.status_code == 201
        assert data["email"] == user_data["email"]
        assert "id" in data

    @pytest.mark.asyncio
    async def test_criar_usuario_email_duplicado(self, client: AsyncClient):
        """Verifica se a API retorna erro ao tentar registar um email que já existe."""
        # Arrange
        user_data = {"email": "duplicado@exemplo.com", "senha": "senha123"}
        await client.post("/usuarios/", json=user_data) # Primeira criação

        # Act
        response = await client.post("/usuarios/", json=user_data) # Segunda tentativa

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Email já registado"}

    @pytest.mark.asyncio
    async def test_login_sucesso(self, client: AsyncClient):
        """Verifica se o login com credenciais corretas retorna um token de acesso."""
        # Arrange
        email = "login@exemplo.com"
        password = "senha_correta"
        await client.post("/usuarios/", json={"email": email, "senha": password})

        # Act
        response = await client.post("/login", data={"username": email, "password": password})
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "access_token" in data
        assert data["token_type"] == "bearer"


class TestTarefas:
    """Testes para o CRUD e lógica de permissões das tarefas."""

    @pytest.mark.asyncio
    async def test_criar_e_listar_tarefas(self, authenticated_client: AuthenticatedClient):
        """Verifica o ciclo completo de criar uma tarefa e depois listá-la."""
        # Arrange
        ac = authenticated_client 
        tarefa_data = {"titulo": "Minha primeira tarefa", "descricao": "Descrição da tarefa"}

        # Act (Listar tarefas quando não há nenhuma)
        response_vazia = await ac.client.get("/tarefas/", headers=ac.headers)
        
        # Assert (A lista deve estar vazia)
        assert response_vazia.status_code == 200
        assert response_vazia.json() == []
        
        # Act (Criar a tarefa)
        response_criacao = await ac.client.post("/tarefas/", json=tarefa_data, headers=ac.headers)
        data_criada = response_criacao.json()

        # Assert (A tarefa foi criada corretamente)
        assert response_criacao.status_code == 201
        assert data_criada["titulo"] == tarefa_data["titulo"]
        assert data_criada["dono_id"] == ac.user_id

        # Act (Listar tarefas novamente)
        response_cheia = await ac.client.get("/tarefas/", headers=ac.headers)
        lista_tarefas = response_cheia.json()

        # Assert (A lista agora contém a tarefa criada)
        assert response_cheia.status_code == 200
        assert len(lista_tarefas) == 1
        assert lista_tarefas[0]["titulo"] == tarefa_data["titulo"]

    @pytest.mark.asyncio
    async def test_utilizador_nao_pode_ver_tarefa_de_outro(self, client: AsyncClient):
        """Garante que um utilizador não consegue aceder a tarefas de outro utilizador."""
        # Arrange: Criar e autenticar o Utilizador A
        user_a_data = {"email": "userA@exemplo.com", "senha": "senha123"}
        await client.post("/usuarios/", json=user_a_data)
        login_a_res = await client.post("/login", data={"username": user_a_data["email"], "password": user_a_data["senha"]})
        headers_a = {"Authorization": f"Bearer {login_a_res.json()['access_token']}"}

        # Arrange: Utilizador A cria uma tarefa
        tarefa_a_res = await client.post("/tarefas/", json={"titulo": "Tarefa do User A"}, headers=headers_a)
        tarefa_a_id = tarefa_a_res.json()["id"]

        # Arrange: Criar e autenticar o Utilizador B
        user_b_data = {"email": "userB@exemplo.com", "senha": "senha456"}
        await client.post("/usuarios/", json=user_b_data)
        login_b_res = await client.post("/login", data={"username": user_b_data["email"], "password": user_b_data["senha"]})
        
        # Assert: Garantir que o login do Utilizador B foi bem sucedido antes de continuar
        assert login_b_res.status_code == 200
        assert "access_token" in login_b_res.json()
        headers_b = {"Authorization": f"Bearer {login_b_res.json()['access_token']}"}

        # Act: Utilizador B tenta aceder à tarefa do Utilizador A
        response_get = await client.get(f"/tarefas/{tarefa_a_id}", headers=headers_b)
        response_put = await client.put(f"/tarefas/{tarefa_a_id}", json={"titulo": "invadido"}, headers=headers_b)
        response_delete = await client.delete(f"/tarefas/{tarefa_a_id}", headers=headers_b)
    
        # Assert: Todas as tentativas devem falhar com erro 403 (Forbidden)
        assert response_get.status_code == 403
        assert response_put.status_code == 403
        assert response_delete.status_code == 403

    @pytest.mark.asyncio
    async def test_acoes_em_tarefa_inexistente_retorna_404(self, authenticated_client: AuthenticatedClient):
        """Verifica se a API retorna 404 ao tentar operar numa tarefa que não existe."""
        # Arrange
        ac = authenticated_client
        id_inexistente = 99999

        # Act
        response_get = await ac.client.get(f"/tarefas/{id_inexistente}", headers=ac.headers)
        response_put = await ac.client.put(f"/tarefas/{id_inexistente}", json={"titulo": "novo"}, headers=ac.headers)
        response_delete = await ac.client.delete(f"/tarefas/{id_inexistente}", headers=ac.headers)
        
        # Assert
        assert response_get.status_code == 404
        assert response_put.status_code == 404
        assert response_delete.status_code == 404