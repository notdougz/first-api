from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .import crud
from .import models
from .import schemas
from .auth import criar_token_de_acesso, get_usuario_atual, verificar_senha, get_db
from .database import lifespan
import os
from datetime import datetime

app = FastAPI(lifespan=lifespan)

# Permite CORS para todas as origens
origins = [
    "https://app-production-8a2c.up.railway.app/",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Geral"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

@app.get("/health", tags=["Geral"])
async def health_check():
    """Endpoint para verificar a saúde da aplicação"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/usuarios/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED, tags=["Utilizadores"])
async def criar_usuario(usuario: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    db_usuario = await crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registado")
    return await crud.create_usuario(db=db, usuario=usuario)

@app.post("/login", tags=["Utilizadores"])
async def login_para_obter_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    usuario = await crud.get_usuario_por_email(db, email=form_data.username)
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = criar_token_de_acesso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tarefas/", response_model=schemas.Tarefa, status_code=status.HTTP_201_CREATED, tags=["Tarefas"])
async def criar_tarefa(
    tarefa: schemas.TarefaCreate,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
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
    tarefas = await crud.get_tarefas_por_usuario(
        db, dono_id=usuario_atual.id, skip=skip, limit=limit
    )
    return tarefas

@app.get("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def ler_tarefa_especifica(
    tarefa_id: int,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
    db_tarefa = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if db_tarefa.dono_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Não tem permissão para aceder a esta tarefa")
    return db_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def atualizar_tarefa(
    tarefa_id: int,
    tarefa: schemas.TarefaCreate,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
    db_tarefa = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if db_tarefa.dono_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Não tem permissão para atualizar esta tarefa")
    return await crud.update_tarefa(db=db, tarefa_id=tarefa_id, tarefa=tarefa)

@app.delete("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def deletar_tarefa(
    tarefa_id: int,
    usuario_atual: models.Usuario = Depends(get_usuario_atual),
    db: AsyncSession = Depends(get_db),
):
    db_tarefa = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if db_tarefa.dono_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Não tem permissão para deletar esta tarefa")
    return await crud.delete_tarefa(db=db, tarefa_id=tarefa_id)