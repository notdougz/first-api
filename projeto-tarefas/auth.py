from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

# --- Configuração de Segurança ---

# Segredos
SECRET_KEY = "firstapi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashing de senhas (reutilizado do crud.py)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança que o FastAPI usará para a documentação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Funções de Autenticação ---
def verificar_senha(senha_plana: str, senha_hash: str):
    """Verifica se a senha fornecida corresponde ao hash guardado."""
    return pwd_context.verify(senha_plana, senha_hash)

def criar_token_de_acesso(data: dict):
    """Cria um novo token de acesso (JWT)."""
    para_codificar = data.copy()
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    para_codificar.update({"exp": expira_em})
    token_codificado = jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_codificado