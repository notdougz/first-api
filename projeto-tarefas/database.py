"""
Módulo de Configuração do Banco de Dados

Este ficheiro é responsável por estabelecer a conexão com o banco de dados,
configurar o motor (engine) do SQLAlchemy e a criação de sessões.
Também define o ciclo de vida (lifespan) da aplicação FastAPI para
criar as tabelas na inicialização.
"""
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Carrega as variáveis de ambiente de um ficheiro .env, se existir.
load_dotenv()

# --- Configuração da URL do Banco de Dados ---

# Obtém a URL do banco de dados a partir das variáveis de ambiente.
# Se `DATABASE_URL` não estiver definida, usa um banco de dados SQLite local
# como fallback, ideal para desenvolvimento e testes.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./tarefas.db")

# Lógica de compatibilidade para o SQLAlchemy 2.0 com asyncpg.
# Garante que a string de conexão para PostgreSQL use o driver `asyncpg`,
# que é necessário para operações assíncronas.
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL and DATABASE_URL.startswith("postgres://"): # comum em serviços como Heroku/Railway
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)


# --- Inicialização do SQLAlchemy ---

# O 'engine' é o ponto central de comunicação com o banco de dados.
engine = create_async_engine(DATABASE_URL)

# 'SessionLocal' é uma fábrica de sessões. Cada instância dela será uma
# sessão de banco de dados individual. Usamos async_sessionmaker para sessões assíncronas.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 'Base' é a classe declarativa da qual todos os nossos modelos de dados (em models.py)
# irão herdar para serem mapeados para tabelas no banco de dados.
Base = declarative_base()


# --- Gestão do Ciclo de Vida da Aplicação (Lifespan) ---

async def create_tables():
    """Cria todas as tabelas no banco de dados se elas ainda não existirem."""
    # Importação local para evitar dependências circulares
    import models
    async with engine.begin() as conn:
        # O run_sync executa a criação das tabelas de forma síncrona dentro do contexto assíncrono.
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para o ciclo de vida da aplicação FastAPI.
    Código aqui é executado antes de a aplicação começar a receber requisições.
    """
    print("Startup: A verificar e a criar tabelas, se necessário...")
    await create_tables()
    yield
    # Código após o 'yield' seria executado no shutdown da aplicação.
    print("Shutdown: Aplicação finalizada.")