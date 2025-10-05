from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from enum import Enum

#Schema Enum para as prioridades
class Prioridade(str, Enum):
    vermelha = "vermelha"
    amarela = "amarela"
    verde = "verde"

# Schema base para a Tarefa
class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False
    
    data_vencimento: Optional[str] = None
    concluida: bool = False

# Schema para a CRIAÇÃO de uma Tarefa (o que a API recebe)
class TarefaCreate(TarefaBase):
    pass

# Schema para a LEITURA de uma Tarefa (o que a API envia de volta)
class Tarefa(TarefaBase):
    id: int
    dono_id: int

    # CORREÇÃO: Usando ConfigDict em vez de class Config
    model_config = ConfigDict(from_attributes=True)
        
class UsuarioBase(BaseModel):
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)