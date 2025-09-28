from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schemas

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

# --- ADICIONE ESTA NOVA FUNÇÃO ---
async def get_tarefas(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de tarefas do banco de dados.
    """
    result = await db.execute(select(models.Tarefa).offset(skip).limit(limit))
    return result.scalars().all()