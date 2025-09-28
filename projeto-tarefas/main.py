# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# 1. Modelo de Dados (Pydantic)
class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False

# Cria a aplicação FastAPI
app = FastAPI()

# 2. "Banco de Dados" em memória
db: List[Tarefa] = []
proximo_id = 1

# 3. Endpoints da API

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

# Endpoint para CRIAR uma nova tarefa (Create)
@app.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa):
    global proximo_id
    tarefa.id = proximo_id
    db.append(tarefa)
    proximo_id += 1
    return tarefa

# Endpoint para LER todas as tarefas (Read)
@app.get("/tarefas/", response_model=List[Tarefa])
def listar_tarefas():
    return db

# Endpoint para LER uma única tarefa por ID (Read)
@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa(tarefa_id: int):
    for tarefa in db:
        if tarefa.id == tarefa_id:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

# Endpoint para ATUALIZAR uma tarefa existente (Update)
@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, tarefa_atualizada: Tarefa):
    for i, tarefa in enumerate(db):
        if tarefa.id == tarefa_id:
            tarefa_atualizada.id = tarefa_id 
            db[i] = tarefa_atualizada
            return tarefa_atualizada
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

# Endpoint para APAGAR uma tarefa (Delete)
@app.delete("/tarefas/{tarefa_id}")
def apagar_tarefa(tarefa_id: int):
    tarefa_para_apagar = None
    for tarefa in db:
        if tarefa.id == tarefa_id:
            tarefa_para_apagar = tarefa
            break
    
    if tarefa_para_apagar:
        db.remove(tarefa_para_apagar)
        return {"message": "Tarefa removida com sucesso"}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")