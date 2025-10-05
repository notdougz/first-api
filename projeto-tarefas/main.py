"""
Ponto de Entrada Principal da API de Gerenciamento de Tarefas

Este módulo define a aplicação FastAPI, configura o CORS, e expõe todos os
endpoints da API para manipulação de utilizadores e tarefas.
"""

# 1. Imports da Biblioteca Padrão
import os
from datetime import datetime
from typing import List

# 2. Imports de Terceiros (Libs)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# 3. Imports Locais da Aplicação
import crud
import models
import schemas
from auth import (
    criar_token_de_acesso,
    get_usuario_atual,
    verificar_senha,
    get_db,
)
from database import lifespan


# --- Configuração da Aplicação FastAPI ---

app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="Uma API para criar, ler, atualizar e deletar tarefas, com autenticação de utilizador.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração de CORS para permitir que o frontend (hospedado em outro domínio)
# possa comunicar com esta API de forma segura.
origins = [
    "https://app-production-8a2c.up.railway.app",  # Domínio de produção
    "http://localhost:8080",                      # Para desenvolvimento local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


# --- Dependência Reutilizável para Validação de Tarefas ---

async def get_tarefa_do_usuario_atual(
    tarefa_id: int,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
) -> models.Tarefa:
    """
    Dependência que busca uma tarefa, garantindo que ela existe e pertence
    ao utilizador atualmente autenticado. Simplifica as rotas de GET, PUT e DELETE.
    """
    db_tarefa = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    if db_tarefa.dono_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não tem permissão para aceder a esta tarefa",
        )
    return db_tarefa


# --- Endpoints Gerais e de Saúde ---

@app.get("/", tags=["Geral"])
def read_root():
    """Endpoint raiz da API."""
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}


@app.get("/health", tags=["Geral"])
async def health_check():
    """
    Verifica a saúde da aplicação. Essencial para sistemas de monitoramento
    e orquestradores como Kubernetes ou Railway.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }


# --- Endpoints de Autenticação e Utilizadores ---

@app.post("/usuarios/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED, tags=["Utilizadores"])
async def criar_usuario(usuario: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """Cria um novo utilizador no sistema."""
    db_usuario = await crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado")
    return await crud.create_usuario(db=db, usuario=usuario)


@app.post("/login", tags=["Utilizadores"])
async def login_para_obter_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Autentica um utilizador e retorna um token de acesso JWT.
    Utiliza OAuth2PasswordRequestForm para seguir o padrão OAuth2.
    """
    usuario = await crud.get_usuario_por_email(db, email=form_data.username)
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = criar_token_de_acesso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- Endpoints de Tarefas (CRUD) ---

@app.post("/tarefas/", response_model=schemas.Tarefa, status_code=status.HTTP_201_CREATED, tags=["Tarefas"])
async def criar_tarefa(
    tarefa: schemas.TarefaCreate,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
    """Cria uma nova tarefa associada ao utilizador autenticado."""
    return await crud.create_tarefa_para_usuario(
        db=db, tarefa=tarefa, dono_id=usuario_atual.id
    )


@app.get("/tarefas/", response_model=List[schemas.Tarefa], tags=["Tarefas"])
async def ler_tarefas_do_usuario(
    skip: int = 0,
    limit: int = 100,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
    """Lista todas as tarefas pertencentes ao utilizador autenticado, com suporte a paginação."""
    tarefas = await crud.get_tarefas_por_usuario(
        db, dono_id=usuario_atual.id, skip=skip, limit=limit
    )
    return tarefas


@app.get("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def ler_tarefa_especifica(
    db_tarefa: models.Tarefa = Depends(get_tarefa_do_usuario_atual),
):
    """Obtém os detalhes de uma tarefa específica."""
    return db_tarefa


@app.put("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def atualizar_tarefa(
    tarefa_atualizada: schemas.TarefaCreate,
    db_tarefa: models.Tarefa = Depends(get_tarefa_do_usuario_atual), # Usando a dependência limpa
    db: AsyncSession = Depends(get_db),
):
    """Atualiza o título, descrição ou status de uma tarefa existente."""
    return await crud.update_tarefa(db=db, db_tarefa=db_tarefa, tarefa_atualizada=tarefa_atualizada)


@app.delete("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def deletar_tarefa(
    db_tarefa: models.Tarefa = Depends(get_tarefa_do_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
    """Remove uma tarefa do banco de dados."""
    return await crud.delete_tarefa(db=db, db_tarefa=db_tarefa)


# --- Bloco de Execução ---

# Este bloco permite executar o servidor de desenvolvimento diretamente
# com `python main.py`, útil para testes rápidos.
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)