"""
Módulo de Modelos de Dados (SQLAlchemy)

Este ficheiro define a estrutura das tabelas do banco de dados utilizando
o ORM do SQLAlchemy. Cada classe aqui representa uma tabela e os seus
atributos correspondem às colunas dessa tabela.
"""
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Usuario(Base):
    """
    Representa a tabela 'usuarios' no banco de dados.

    Armazena as informações de login de um utilizador.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    # --- Relacionamentos ---
    # Define a relação "um-para-muitos" com a tabela de tarefas.
    # O 'back_populates' cria a ligação bidirecional com o relacionamento 'dono' na classe Tarefa.
    # O 'cascade' garante que, se um utilizador for apagado, todas as suas tarefas também o sejam.
    tarefas = relationship("Tarefa", back_populates="dono", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}')>"


class Tarefa(Base):
    """
    Representa a tabela 'tarefas' no banco de dados.

    Armazena os detalhes de uma tarefa, que está sempre associada a um utilizador.
    """
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False, nullable=False)
    data_vencimento = Column(Date, nullable=True)
    prioridade = Column(String, default="verde", nullable=False)

    # --- Chaves Estrangeiras e Relacionamentos ---
    # Define a coluna que armazena o ID do utilizador dono da tarefa.
    dono_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Cria a referência de volta para o objeto Usuario correspondente.
    # O 'back_populates' liga este relacionamento ao 'tarefas' na classe Usuario.
    dono = relationship("Usuario", back_populates="tarefas")

    def __repr__(self):
        return f"<Tarefa(id={self.id}, titulo='{self.titulo}')>"