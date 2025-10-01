# API de Gerenciamento de Tarefas

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=flat-square&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=flat-square&logo=sqlite)

## 📝 Sobre o Projeto

API REST desenvolvida com FastAPI para gerenciar uma lista de tarefas (To-Do list). Cada usuário tem suas próprias tarefas privadas, protegidas por autenticação JWT.

**Principais recursos:**
- Sistema de autenticação completo (registro, login, JWT)
- CRUD completo de tarefas (criar, ler, atualizar, deletar)
- Banco de dados SQLite com SQLAlchemy
- Cada usuário só acessa suas próprias tarefas
- Documentação automática da API

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/notdougz/first-api.git
cd first-api/projeto-tarefas
```

2. **Crie o ambiente virtual:**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> 💡 **Gere uma SECRET_KEY segura com:**
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

5. **Execute a API:**
```bash
uvicorn main:app --reload
```

6. **Acesse:**
- API: `http://127.0.0.1:8000`
- Documentação: `http://127.0.0.1:8000/docs`

## 📚 Endpoints da API

| Método | Endpoint | Descrição | Requer Auth |
|--------|----------|-----------|-------------|
| `POST` | `/usuarios/` | Registrar novo usuário | ❌ |
| `POST` | `/login` | Fazer login e obter token | ❌ |
| `POST` | `/tarefas/` | Criar tarefa | ✅ |
| `GET` | `/tarefas/` | Listar minhas tarefas | ✅ |
| `GET` | `/tarefas/{id}` | Ver tarefa específica | ✅ |
| `PUT` | `/tarefas/{id}` | Atualizar tarefa | ✅ |
| `DELETE` | `/tarefas/{id}` | Deletar tarefa | ✅ |

## 🔧 Como Usar

### 1. Registrar usuário
```bash
curl -X POST "http://127.0.0.1:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com", "senha": "sua_senha"}'
```

### 2. Fazer login
```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu@email.com&password=sua_senha"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 3. Criar tarefa (use o token obtido)
```bash
curl -X POST "http://127.0.0.1:8000/tarefas/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"titulo": "Estudar FastAPI", "descricao": "Aprender sobre APIs", "concluida": false}'
```

### 4. Listar tarefas
```bash
curl -X GET "http://127.0.0.1:8000/tarefas/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🏗️ Estrutura do Projeto

```
projeto-tarefas/
│
├── main.py              # Aplicação principal e rotas
├── database.py          # Configuração do banco de dados
├── models.py            # Modelos SQLAlchemy (tabelas)
├── schemas.py           # Validação de dados (Pydantic)
├── crud.py              # Operações no banco de dados
├── auth.py              # Autenticação e segurança
├── .env                 # Variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo Git
├── requirements.txt     # Dependências do projeto
├── tarefas.db           # Banco de dados (criado automaticamente)
└── tests/               # Testes automatizados
    ├── __init__.py
    ├── test_database.py
    └── test_main.py
```

## 🧪 Executar Testes

```bash
pytest
```

## 🔒 Segurança

- ✅ Senhas criptografadas com bcrypt
- ✅ Autenticação JWT com tokens de acesso
- ✅ Isolamento de dados por usuário
- ✅ Validação automática de dados
- ✅ SECRET_KEY em variável de ambiente

## 💻 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados leve
- **JWT** - Autenticação segura
- **Pydantic** - Validação de dados
- **Pytest** - Testes automatizados

## 📖 Testar na Documentação Interativa

1. Acesse `http://127.0.0.1:8000/docs`
2. Registre um usuário em `POST /usuarios/`
3. Faça login em `POST /login` e copie o token
4. Clique em **"Authorize"** no topo da página
5. Cole o token e confirme
6. Agora você pode testar todos os endpoints!

## 🎯 Próximas Melhorias

- [ ] Adicionar datas de criação/atualização
- [ ] Implementar filtros (concluídas/pendentes)
- [ ] Sistema de categorias/tags
- [ ] Prioridades nas tarefas
- [ ] Datas de vencimento

## 👤 Autor

**Douglas** - [@notdougz](https://github.com/notdougz)

## 📄 Licença

Projeto de código aberto para fins educacionais.

---

⭐ Se este projeto te ajudou, considere dar uma estrela!

## 📚 Recursos de Aprendizagem

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial JWT](https://jwt.io/introduction)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
