"""
Módulo de Configuração do Banco de Dados para Testes

Este ficheiro cria uma configuração de banco de dados específica para a suíte
de testes do Pytest. O objetivo é garantir que os testes sejam executados
num ambiente isolado, previsível e rápido.
"""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# --- Configuração da URL do Banco de Dados de Teste ---

# Define a URL para um banco de dados SQLite a ser executado em memória.
# Vantagens de usar "in-memory":
# 1. Rapidez: Não há operações de disco, tornando os testes muito mais rápidos.
# 2. Isolamento: O banco de dados é criado do zero a cada execução da suíte de testes
#    e destruído ao final, garantindo que os testes não interfiram uns com os outros.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# --- Inicialização do SQLAlchemy para Testes ---

# Cria o motor (engine) assíncrono para o banco de dados de teste.
# `connect_args={"check_same_thread": False}` é uma configuração específica
# e necessária para o funcionamento do SQLite com o FastAPI.
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões de teste.
# Esta será usada para criar sessões de banco de dados para os testes,
# permitindo que cada teste tenha a sua própria transação isolada.
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos de teste.
# É a mesma base que a aplicação usa, para que as tabelas sejam criadas corretamente.
Base = declarative_base()