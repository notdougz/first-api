# tests/test_main.py

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base
import pytest

# --- Configuração do Banco de Dados de Teste Síncrono ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 'engine' síncrono para os testes
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no início dos testes
Base.metadata.create_all(bind=engine)

# --- Sobrescreve a dependência get_db para usar o banco de teste ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- Cria o cliente de teste ---
client = TestClient(app)

# --- O Nosso Primeiro Teste 
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}
