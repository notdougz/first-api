from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schemas

async def get_tarefa(db: AsyncSession, tarefa_id: int):
    """
    Busca e retorna uma única tarefa pelo seu ID.
    """
    result = await db.execute(select(models.Tarefa).filter(models.Tarefa.id == tarefa_id))
    return result.scalar_one_or_none()

async def update_tarefa(db: AsyncSession, tarefa_id: int, tarefa: schemas.TarefaCreate):
    """
    Atualiza uma tarefa existente no banco de dados.
    """
    db_tarefa = await get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa:
        # Atualiza os campos do objeto com os novos dados
        db_tarefa.titulo = tarefa.titulo
        db_tarefa.descricao = tarefa.descricao
        db_tarefa.concluida = tarefa.concluida
        # Confirma as mudanças no banco
        await db.commit()
        await db.refresh(db_tarefa)
    return db_tarefa

async def delete_tarefa(db: AsyncSession, tarefa_id: int):
    """
    Apaga uma tarefa do banco de dados.
    """
    db_tarefa = await get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa:
        # Apaga o objeto do banco
        await db.delete(db_tarefa)
        await db.commit()
    return db_tarefa

async def create_tarefa(db: AsyncSession, tarefa: schemas.TarefaCreate):
    """
    Cria uma nova tarefa no banco de dados.
    """
    # 1. Cria um objeto do modelo SQLAlchemy a partir dos dados recebidos.
    db_tarefa = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        concluida=tarefa.concluida
    )
    # 2. Adiciona o objeto à sessão do banco de dados.
    db.add(db_tarefa)
    # 3. Confirma (salva) as mudanças no banco.
    await db.commit()
    # 4. Atualiza o objeto com os novos dados do banco (como o ID).
    await db.refresh(db_tarefa)
    return db_tarefa

async def get_tarefas(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de tarefas do banco de dados.
    """
    result = await db.execute(select(models.Tarefa).offset(skip).limit(limit))
    return result.scalars().all()