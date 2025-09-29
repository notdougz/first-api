from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import crud
import schemas
from database import SessionLocal, lifespan

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

# --- Endpoints da API ---
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

# --- NOVO ENDPOINT DE CRIAÇÃO ---
@app.post("/tarefas/", response_model=schemas.Tarefa, status_code=201)
async def criar_nova_tarefa(
    tarefa: schemas.TarefaCreate, db: AsyncSession = Depends(get_db)
):
    """
    Cria uma nova tarefa no banco de dados.
    """
    return await crud.create_tarefa(db=db, tarefa=tarefa)

# --- ENDPOINT PARA LER TODAS AS TAREFAS (CORRIGIDO) ---
@app.get("/tarefas/", response_model=List[schemas.Tarefa])
async def listar_todas_as_tarefas(db: AsyncSession = Depends(get_db)):
    """
    Retorna uma lista de todas as tarefas do banco de dados.
    """
    tarefas = await crud.get_tarefas(db=db)
    return tarefas
