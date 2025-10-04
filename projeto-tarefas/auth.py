import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal

# --- Configuração de Segurança ---
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "Denbinsk4853@")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Funções de Autenticação ---
def verificar_senha(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)

def criar_token_de_acesso(data: dict):
    para_codificar = data.copy()
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    para_codificar.update({"exp": expira_em})
    token_codificado = jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_codificado

# Dependência para obter uma sessão do banco de dados
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# A nossa "guarda de segurança"
async def get_usuario_atual(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    import crud
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    usuario = await crud.get_usuario_por_email(db, email=email)
    if usuario is None:
        raise credentials_exception
    return usuario