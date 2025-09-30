from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import crud
import models 
import schemas
from database import SessionLocal, lifespan
from fastapi.security import OAuth2PasswordRequestForm
import auth
from auth import get_usuario_atual

# --- Configuração da Aplicação FastAPI ---
app = FastAPI(lifespan=lifespan)

# --- Dependência para obter a Sessão do Banco de Dados ---
# Esta função será chamada em cada endpoint que precisar acessar o banco.
# O FastAPI gerencia a abertura e o fechamento da conexão.
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
            
@app.get("/", tags=["Geral"])
def read_root():
    """
    Retorna uma mensagem de boas-vindas à API.
    """
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

@app.post("/tarefas/", response_model=schemas.Tarefa, status_code=201, tags=["Tarefas"])
async def criar_nova_tarefa(
    tarefa: schemas.TarefaCreate, 
    db: AsyncSession = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_usuario_atual)
):
    """
    Cria uma nova tarefa para o utilizador atualmente logado.
    """
    return await crud.create_tarefa_para_usuario(db=db, tarefa=tarefa, dono_id=usuario_logado.id)

@app.get("/tarefas/", response_model=List[schemas.Tarefa], tags=["Tarefas"])
async def listar_tarefas_do_usuario(
    db: AsyncSession = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_usuario_atual)
):
    """
    Retorna uma lista de todas as tarefas do utilizador logado.
    """
    return await crud.get_tarefas_por_usuario(db=db, dono_id=usuario_logado.id)

@app.get("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def ler_tarefa_por_id(
    tarefa_id: int, 
    db: AsyncSession = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_usuario_atual)
):
    """
    Retorna uma tarefa específica, se pertencer ao utilizador logado.
    """
    db_tarefa = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None or db_tarefa.dono_id != usuario_logado.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def atualizar_tarefa_por_id(
    tarefa_id: int, 
    tarefa: schemas.TarefaCreate, 
    db: AsyncSession = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_usuario_atual)
):
    """
    Atualiza uma tarefa, se pertencer ao utilizador logado.
    """
    db_tarefa_existente = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa_existente is None or db_tarefa_existente.dono_id != usuario_logado.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return await crud.update_tarefa(db, tarefa_id=tarefa_id, tarefa=tarefa)

@app.delete("/tarefas/{tarefa_id}", response_model=schemas.Tarefa, tags=["Tarefas"])
async def apagar_tarefa_por_id(
    tarefa_id: int, 
    db: AsyncSession = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_usuario_atual)
):
    """
    Apaga uma tarefa, se pertencer ao utilizador logado.
    """
    db_tarefa_existente = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa_existente is None or db_tarefa_existente.dono_id != usuario_logado.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return await crud.delete_tarefa(db, tarefa_id=tarefa_id)