"""
Módulo de Schemas Pydantic

Este ficheiro define os "contratos de dados" da API. Os schemas Pydantic
são usados para validar os dados das requisições recebidas (input) e para
formatar os dados das respostas enviadas (output).

Isto garante que a comunicação entre o cliente e o servidor seja previsível e segura.
"""
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- Enums ---

class Prioridade(str, Enum):
    """Define os valores permitidos para a prioridade de uma tarefa."""
    vermelha = "vermelha"
    amarela = "amarela"
    verde = "verde"


# --- Schemas para Utilizadores ---

class UsuarioBase(BaseModel):
    """Schema base com os campos comuns de um utilizador."""
    email: EmailStr  # Usa EmailStr para validar automaticamente o formato do email.


class UsuarioCreate(UsuarioBase):
    """
    Schema usado para a criação de um novo utilizador.
    Recebe a senha em texto plano, que será hasheada antes de ser guardada.
    """
    senha: str = Field(..., min_length=8, description="A senha deve ter no mínimo 8 caracteres.")


class Usuario(UsuarioBase):
    """
    Schema usado para retornar os dados de um utilizador.
    Importante: NÃO inclui a senha.
    """
    id: int

    model_config = ConfigDict(
        from_attributes=True,  # Permite que o Pydantic leia os dados de um objeto SQLAlchemy.
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "joao.silva@exemplo.com",
            }
        }
    )


# --- Schemas para Tarefas ---

class TarefaBase(BaseModel):
    """Schema base com os campos comuns de uma tarefa."""
    titulo: str = Field(..., max_length=100, description="O título da tarefa.")
    descricao: Optional[str] = Field(None, max_length=500, description="A descrição detalhada da tarefa.")
    concluida: bool = False
    data_vencimento: Optional[date] = None
    prioridade: Prioridade = Prioridade.verde


class TarefaCreate(TarefaBase):
    """
    Schema usado para criar uma nova tarefa. Herda todos os campos da base.
    O `pass` indica que não há campos adicionais necessários para a criação.
    """
    pass


class Tarefa(TarefaBase):
    """
    Schema usado para retornar os dados de uma tarefa.
    Inclui campos gerados pelo banco de dados, como 'id' e 'dono_id'.
    """
    id: int
    dono_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 101,
                "dono_id": 1,
                "titulo": "Finalizar relatório do projeto",
                "descricao": "Compilar os dados do Q3 e criar os gráficos.",
                "concluida": False,
                "data_vencimento": "2025-10-15",
                "prioridade": "vermelha",
            }
        }
    )