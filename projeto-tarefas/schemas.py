from pydantic import BaseModel
from typing import Optional, List

# Schema base para a Tarefa (campos comuns)
class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False

# Schema para a CRIAÇÃO de uma Tarefa (o que a API recebe)
# Não precisa de ID, pois o banco de dados irá gerá-lo.
class TarefaCreate(TarefaBase):
    pass

# Schema para a LEITURA de uma Tarefa (o que a API envia de volta)
# Inclui o ID e permite que o Pydantic leia dados de objetos do SQLAlchemy.
class Tarefa(TarefaBase):
    id: int
    dono_id: int

    class Config:
        from_attributes = True
        
class UsuarioBase(BaseModel):
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True