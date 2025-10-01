# Mude para este código em schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Schema base para a Tarefa (campos comuns)
class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
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
    
    # CORREÇÃO: Usando ConfigDict em vez de class Config
    model_config = ConfigDict(from_attributes=True)