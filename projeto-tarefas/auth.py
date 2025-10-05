"""
Módulo de Autenticação e Segurança

Este ficheiro contém toda a lógica relacionada com a autenticação de utilizadores,
incluindo a verificação de senhas, criação de tokens JWT e a dependência
para proteger os endpoints da API.
"""

# 1. Imports da Biblioteca Padrão
import os
from datetime import datetime, timedelta, timezone

# 2. Imports de Terceiros (Libs)
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

# 3. Imports Locais da Aplicação
from database import SessionLocal

if TYPE_CHECKING:
    import models

# --- Configuração de Segurança e Variáveis de Ambiente ---

# Carrega as variáveis de ambiente do ficheiro .env para o ambiente do sistema
load_dotenv()

# Chave secreta usada para assinar os tokens JWT. É crucial que seja mantida segura.
SECRET_KEY = os.getenv("SECRET_KEY")
# Algoritmo de assinatura do token. HS256 é um padrão comum e seguro.
ALGORITHM = "HS256"
# Tempo de vida do token de acesso em minutos.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# --- Contexto de Hashing e Esquema OAuth2 ---

# Configura o Passlib para usar bcrypt como o algoritmo de hashing de senhas.
# O "deprecated='auto'" garante a atualização automática de hashes se um novo padrão for definido.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cria uma instância do OAuth2PasswordBearer.
# O FastAPI usa isto para extrair o token do cabeçalho "Authorization" das requisições.
# O "tokenUrl='login'" aponta para o nosso endpoint de login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- Funções Utilitárias de Autenticação ---

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara uma senha em texto plano com o seu hash armazenado de forma segura."""
    return pwd_context.verify(senha_plana, senha_hash)


def criar_token_de_acesso(data: dict) -> str:
    """
    Cria um novo token de acesso JWT.

    Args:
        data: Um dicionário com os dados a serem incluídos no "payload" do token.
              Normalmente contém o identificador do utilizador (o 'subject').

    Returns:
        O token JWT codificado como uma string.
    """
    para_codificar = data.copy()
    # Define o tempo de expiração do token (agora + 30 minutos)
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    para_codificar.update({"exp": expira_em})
    # Codifica o payload usando a chave secreta e o algoritmo definidos
    token_codificado = jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_codificado


# --- Dependências da Aplicação ---

async def get_db():
    """
    Dependência do FastAPI que cria e fornece uma sessão de banco de dados
    para uma requisição e garante que ela seja fechada ao final.
    """
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def get_usuario_atual(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> "models.Usuario":
    """
    Dependência "guarda de segurança". Verifica a validade do token JWT
    e retorna o utilizador correspondente. Se o token for inválido ou
    o utilizador não existir, levanta uma exceção HTTP 401.
    """
    # Importação local para evitar dependência circular
    # (crud.py pode precisar importar algo de auth.py no futuro)
    import crud
    import models

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token para aceder ao payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # O "sub" (subject) do nosso token é o email do utilizador
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # Se a decodificação falhar (token inválido, expirado, etc.), levanta a exceção
        raise credentials_exception

    # Com o email extraído, busca o utilizador no banco de dados
    usuario = await crud.get_usuario_por_email(db, email=email)
    if usuario is None:
        # Se o utilizador não for encontrado no banco, o token não é mais válido
        raise credentials_exception

    return usuario