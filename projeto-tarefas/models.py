from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False)