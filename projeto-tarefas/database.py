import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente de um arquivo .env (útil para desenvolvimento local)
load_dotenv()

# Usa a DATABASE_URL do ambiente, com um fallback para o SQLite local
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./tarefas.db")

# Lógica para substituir 'postgres://' por 'postgresql://' se necessário,
# pois algumas plataformas (como Heroku/Railway) usam o primeiro formato.
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
    # A linha abaixo só é necessária para SQLite
    # connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def create_tables():
    from . import models 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Verificando e criando tabelas, se necessário...")
    await create_tables()
    yield
    print("Aplicação finalizada.")