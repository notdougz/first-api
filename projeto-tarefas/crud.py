"""
Módulo de Operações CRUD (Create, Read, Update, Delete)

Este ficheiro centraliza toda a lógica de interação com o banco de dados.
Cada função aqui é responsável por uma operação atómica na base de dados,
mantendo a camada de API (main.py) limpa e focada na lógica de negócio.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from auth import pwd_context


# --- Funções CRUD para Utilizadores ---

async def get_usuario_por_email(db: AsyncSession, email: str) -> models.Usuario | None:
    """
    Busca e retorna um utilizador pelo seu email.

    Args:
        db: A sessão assíncrona do banco de dados.
        email: O email do utilizador a ser procurado.

    Returns:
        O objeto do modelo Usuario ou None se não for encontrado.
    """
    result = await db.execute(select(models.Usuario).filter(models.Usuario.email == email))
    return result.scalar_one_or_none()


async def create_usuario(db: AsyncSession, usuario: schemas.UsuarioCreate) -> models.Usuario:
    """
    Cria um novo utilizador no banco de dados com a senha encriptada.

    Args:
        db: A sessão assíncrona do banco de dados.
        usuario: O objeto Pydantic com os dados do novo utilizador.

    Returns:
        O objeto do modelo Usuario recém-criado.
    """
    senha_hash = pwd_context.hash(usuario.senha)
    db_usuario = models.Usuario(email=usuario.email, senha_hash=senha_hash)

    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario


# --- Funções CRUD para Tarefas ---

async def get_tarefa(db: AsyncSession, tarefa_id: int) -> models.Tarefa | None:
    """
    Busca e retorna uma única tarefa pelo seu ID.

    Args:
        db: A sessão assíncrona do banco de dados.
        tarefa_id: O ID da tarefa a ser procurada.

    Returns:
        O objeto do modelo Tarefa ou None se não for encontrado.
    """
    result = await db.execute(select(models.Tarefa).filter(models.Tarefa.id == tarefa_id))
    return result.scalar_one_or_none()


async def get_tarefas_por_usuario(db: AsyncSession, dono_id: int, skip: int = 0, limit: int = 100) -> list[models.Tarefa]:
    """
    Retorna uma lista de tarefas de um utilizador específico, com suporte a paginação.

    Args:
        db: A sessão assíncrona do banco de dados.
        dono_id: O ID do utilizador dono das tarefas.
        skip: O número de registos a pular (para paginação).
        limit: O número máximo de registos a retornar.

    Returns:
        Uma lista de objetos do modelo Tarefa.
    """
    result = await db.execute(
        select(models.Tarefa)
        .filter(models.Tarefa.dono_id == dono_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_tarefa_para_usuario(db: AsyncSession, tarefa: schemas.TarefaCreate, dono_id: int) -> models.Tarefa:
    """
    Cria uma nova tarefa no banco de dados, associada a um utilizador.

    Args:
        db: A sessão assíncrona do banco de dados.
        tarefa: O objeto Pydantic com os dados da nova tarefa.
        dono_id: O ID do utilizador que será o dono da tarefa.

    Returns:
        O objeto do modelo Tarefa recém-criado.
    """
    # Cria a instância do modelo SQLAlchemy a partir dos dados do schema Pydantic
    db_tarefa = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        concluida=tarefa.concluida,
        data_vencimento=tarefa.data_vencimento,
        prioridade=tarefa.prioridade.value,  # Pega o valor do Enum
        dono_id=dono_id
    )
    # Adiciona à sessão, commita e atualiza para obter o ID gerado
    db.add(db_tarefa)
    await db.commit()
    await db.refresh(db_tarefa)
    return db_tarefa


async def update_tarefa(
    db: AsyncSession, db_tarefa: models.Tarefa, tarefa_atualizada: schemas.TarefaCreate
) -> models.Tarefa:
    """Atualiza uma tarefa existente no banco de dados."""
    db_tarefa.titulo = tarefa_atualizada.titulo
    db_tarefa.descricao = tarefa_atualizada.descricao
    db_tarefa.concluida = tarefa_atualizada.concluida
    db_tarefa.data_vencimento = tarefa_atualizada.data_vencimento
    db_tarefa.prioridade = tarefa_atualizada.prioridade.value
    await db.commit()
    await db.refresh(db_tarefa)
    return db_tarefa


async def delete_tarefa(db: AsyncSession, db_tarefa: models.Tarefa) -> models.Tarefa:
    """
    Apaga uma tarefa do banco de dados.

    Args:
        db: A sessão assíncrona do banco de dados.
        db_tarefa: O objeto SQLAlchemy da tarefa a ser deletada (já validado).

    Returns:
        O objeto da tarefa que foi deletada.
    """
    await db.delete(db_tarefa)
    await db.commit()
    return db_tarefa