from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String) # NUNCA guardamos a senha em texto!

    # Esta linha cria a relação: um utilizador pode ter muitas tarefas.
    tarefas = relationship("Tarefa", back_populates="dono")

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False)
    # Esta é a chave estrangeira que liga a tarefa ao utilizador.
    dono_id = Column(Integer, ForeignKey("usuarios.id"))

    # Esta linha completa a relação com a tabela de utilizadores.
    dono = relationship("Usuario", back_populates="tarefas")