from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import crud
import schemas
from database import SessionLocal, lifespan
from fastapi.security import OAuth2PasswordRequestForm
import auth

# --- Configuração da Aplicação FastAPI ---
app = FastAPI(lifespan=lifespan)

# --- Dependência para obter a Sessão do Banco de Dados ---
# Esta função será chamada em cada endpoint que precisar acessar o banco.
# O FastAPI gerencia a abertura e o fechamento da conexão.
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# --- Endpoints da API ---
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Tarefas!"}

@app.post("/tarefas/", response_model=schemas.Tarefa, status_code=201)
async def criar_nova_tarefa(
    tarefa: schemas.TarefaCreate, db: AsyncSession = Depends(get_db)
):
    """
    Cria uma nova tarefa no banco de dados.
    """
    return await crud.create_tarefa(db=db, tarefa=tarefa)

@app.get("/tarefas/", response_model=List[schemas.Tarefa])
async def listar_todas_as_tarefas(db: AsyncSession = Depends(get_db)):
    """
    Retorna uma lista de todas as tarefas do banco de dados.
    """
    tarefas = await crud.get_tarefas(db=db)
    return tarefas

@app.get("/tarefas/{tarefa_id}", response_model=schemas.Tarefa)
async def ler_tarefa_por_id(tarefa_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retorna uma tarefa específica buscando pelo seu ID.
    """
    db_tarefa = await crud.get_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=schemas.Tarefa)
async def atualizar_tarefa_por_id(
    tarefa_id: int, tarefa: schemas.TarefaCreate, db: AsyncSession = Depends(get_db)
):
    """
    Atualiza os dados de uma tarefa existente.
    """
    db_tarefa = await crud.update_tarefa(db, tarefa_id=tarefa_id, tarefa=tarefa)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}", response_model=schemas.Tarefa)
async def apagar_tarefa_por_id(tarefa_id: int, db: AsyncSession = Depends(get_db)):
    """
    Apaga uma tarefa do banco de dados.
    """
    db_tarefa = await crud.delete_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.post("/usuarios/", response_model=schemas.Usuario)
async def criar_novo_usuario(
    usuario: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)
):
    """
    Registra um novo utilizador no sistema.
    """
    db_usuario = await crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return await crud.create_usuario(db=db, usuario=usuario)

@app.post("/login")
async def login_para_obter_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Autentica um utilizador e retorna um token de acesso.
    """
    # 1. Procura o utilizador pelo email (que no formulário vem como 'username')
    usuario = await crud.get_usuario_por_email(db, email=form_data.username)

    # 2. Verifica se o utilizador existe e se a senha está correta
    if not usuario or not auth.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Cria o token de acesso
    access_token = auth.criar_token_de_acesso(
        data={"sub": usuario.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}