from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)

    # Esta linha cria a relação: um utilizador pode ter muitas tarefas.
    tarefas = relationship("Tarefa", back_populates="dono")

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False)
    data_vencimento = Column(Date, nullable=True)
    prioridade = Column(String, default="verde") 
    dono_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("Usuario", back_populates="tarefas")