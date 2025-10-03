# 📋 Gerenciador de Tarefas – Full‑Stack (FastAPI + JS)

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square&logo=docker)
![Railway](https://img.shields.io/badge/Deploy-Railway-purple?style=flat-square)

Aplicação full‑stack de gerenciamento de tarefas com autenticação JWT, focada em boas práticas e deploy em produção.

### 🔥 Demonstração (Produção)

- 🌐 App em produção: [`app-production-8a2c.up.railway.app`](https://app-production-8a2c.up.railway.app/)

> Frontend estático (Nginx) consumindo API FastAPI com CORS liberado para o domínio de produção.

#### 👀 Prévia visual

![Tela de Login](login.png)

![Minhas Tarefas](tarefas.png)

## 🎯 Visão Geral

Projeto construído para consolidar conhecimentos de backend, frontend e DevOps. Traz uma base sólida e organizada, ideal para evolução (novas features, migração de banco, CI/CD etc.).

### 🚀 Destaques Técnicos

- **Backend**: FastAPI, autenticação JWT, ORM SQLAlchemy (async)
- **Frontend**: HTML/CSS/JS (vanilla) responsivo, UX simples e direto
- **Segurança**: hash de senha (Passlib), tokens JWT, escopo por usuário
- **Qualidade**: testes com Pytest, tipagem Pydantic, validações
- **DevOps**: Docker, Docker Compose e deploy em Railway

## 🛠️ Funcionalidades

- ✅ Registro e login de usuários
- ✅ Criar, listar, editar e excluir tarefas do usuário autenticado
- ✅ Tema claro/escuro e feedback visual
- ✅ Documentação automática da API (Swagger)

## ⚡ Como Rodar

### Opção 1: Docker Compose (Recomendado)

```bash
# Clone o projeto
git clone https://github.com/notdougz/first-api.git
cd first-api

# Sobe API e Frontend
docker-compose up --build
```

Acesse:

- 🌐 Frontend: http://localhost:8080
- 🔧 API: http://localhost:8000
- 📚 Docs: http://localhost:8000/docs

### Opção 2: Execução Local (Desenvolvimento)

```bash
cd projeto-tarefas

# Instala dependências
pip install -r requirements.txt

# Executa API
uvicorn main:app --reload
```

## 🔑 Variáveis de Ambiente

Copie `env.example` para `.env` e ajuste conforme o ambiente.

Mínimo para desenvolvimento (SQLite padrão):

```
SECRET_KEY="sua_chave_secreta_super_segura"
ENVIRONMENT=development
```

Produção (ex.: `docker-compose.prod.yml` usa PostgreSQL):

```
POSTGRES_DB=tarefas_db
POSTGRES_USER=tarefas_user
POSTGRES_PASSWORD=tarefas_password
SECRET_KEY=sua_chave_secreta_super_segura
ENVIRONMENT=production
```

## 📦 Endpoints Principais

- `POST /usuarios/` – cria usuário
- `POST /login` – retorna `access_token`
- `GET /tarefas/` – lista tarefas do usuário
- `POST /tarefas/` – cria tarefa
- `GET /tarefas/{id}` – detalhe
- `PUT /tarefas/{id}` – atualização
- `DELETE /tarefas/{id}` – remoção
- `GET /health` – verificação de saúde

Autenticação via Bearer Token (`Authorization: Bearer <token>`).

## 🧪 Testes

```bash
cd projeto-tarefas
pytest
```

## 🏗️ Arquitetura

```
first-api/
├── docker-compose.yml           # Dev (API + Frontend)
├── docker-compose.prod.yml      # Prod (API + Postgres + Frontend)
├── projeto-tarefas/             # Backend (FastAPI)
│   ├── main.py                  # Rotas e CORS
│   ├── auth.py                  # JWT, hashing e dependências
│   ├── crud.py                  # Operações de banco
│   ├── models.py                # Modelos SQLAlchemy
│   ├── schemas.py               # Pydantic
│   └── tests/                   # Pytest
└── frontend/                    # Frontend estático
    ├── index.html
    ├── app.js
    └── style.css
```

## 🔒 CORS e Domínios

O backend permite CORS para:

- `https://app-production-8a2c.up.railway.app`
- `http://localhost:8080`

Isso garante que o frontend em produção e local acessem a API com segurança.

## 🚀 Deploy

- Infra de produção hospedada na Railway.
- Compose de produção inclui Postgres, API e Frontend Nginx.
- Healthcheck em `GET /health` para orquestração e observabilidade.

## 💻 Stack Tecnológica

**Backend**: FastAPI, SQLAlchemy (async), Pydantic, JWT, Passlib

**Frontend**: HTML5, CSS3, JavaScript ES6+, Fetch API

**DevOps**: Docker, Docker Compose, Railway

## 👤 Autor

**Douglas** – [@notdougz](https://github.com/notdougz)

_Projeto desenvolvido como parte do meu aprendizado em desenvolvimento full‑stack._

---

Se este projeto foi útil, deixe uma ⭐ e compartilhe!
