# 📋 Gerenciador de Tarefas - Projeto de Aprendizagem

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square&logo=docker)

## 🎯 Sobre o Projeto

Este é um projeto **full-stack** que desenvolvi para aprender e praticar tecnologias modernas de desenvolvimento web. É uma aplicação completa de gerenciamento de tarefas com autenticação de usuários.

### 🚀 O que aprendi construindo este projeto:

- **Backend**: API REST com FastAPI, autenticação JWT, ORM com SQLAlchemy
- **Frontend**: Interface responsiva com JavaScript vanilla e CSS moderno
- **DevOps**: Containerização com Docker e Docker Compose
- **Testes**: Testes automatizados com Pytest
- **Segurança**: Hash de senhas, tokens JWT, isolamento de dados por usuário

## ⚡ Execução Rápida com Docker

### Opção 1: Docker Compose (Recomendado)

```bash
# Clone o projeto
git clone https://github.com/notdougz/first-api.git
cd first-api

# Execute tudo com um comando
docker-compose up --build
```

**Pronto!** Acesse:

- 🌐 **Frontend**: http://localhost:8080
- 🔧 **API**: http://localhost:8000
- 📚 **Documentação**: http://localhost:8000/docs

### Opção 2: Execução Local (Desenvolvimento)

```bash
cd projeto-tarefas

# Instale as dependências
pip install -r requirements.txt

# Execute a API
uvicorn main:app --reload
```

## 🛠️ Funcionalidades

### Frontend (Interface Web)

- ✅ **Autenticação**: Login e registro de usuários
- ✅ **CRUD de Tarefas**: Criar, visualizar, editar e excluir tarefas
- ✅ **Interface Responsiva**: Design moderno que funciona em desktop e mobile
- ✅ **Tema Escuro/Claro**: Alternância de temas
- ✅ **Feedback Visual**: Mensagens de sucesso e erro

### Backend (API REST)

- ✅ **Autenticação JWT**: Tokens seguros para autenticação
- ✅ **Banco de Dados**: SQLite com SQLAlchemy (async)
- ✅ **Validação**: Pydantic para validação automática de dados
- ✅ **Documentação**: Swagger UI automática
- ✅ **Testes**: Cobertura de testes com Pytest

## 🧪 Executar Testes

```bash
cd projeto-tarefas
pytest
```

## 🏗️ Arquitetura do Projeto

```
first-api/
├── 🐳 docker-compose.yml    # Orquestração dos containers
├── 📁 projeto-tarefas/      # Backend (FastAPI)
│   ├── main.py              # Rotas da API
│   ├── models.py            # Modelos do banco de dados
│   ├── auth.py              # Sistema de autenticação
│   ├── crud.py              # Operações no banco
│   └── tests/               # Testes automatizados
└── 📁 frontend/             # Frontend (HTML/CSS/JS)
    ├── index.html           # Interface principal
    ├── app.js               # Lógica do frontend
    └── style.css            # Estilos responsivos
```

## 💻 Stack Tecnológica

### Backend

- **FastAPI** - Framework web async/await
- **SQLAlchemy** - ORM com suporte async
- **SQLite** - Banco de dados leve
- **JWT** - Autenticação stateless
- **Pytest** - Testes automatizados

### Frontend

- **HTML5/CSS3** - Estrutura e estilos
- **JavaScript ES6+** - Interatividade
- **Fetch API** - Comunicação com a API

### DevOps

- **Docker** - Containerização
- **Docker Compose** - Orquestração multi-container

## 🎓 Aprendizados Principais

Durante o desenvolvimento deste projeto, pratiquei conceitos importantes como:

- **APIs RESTful** e padrões HTTP
- **Autenticação JWT** e segurança web
- **Programação assíncrona** com Python
- **Containerização** e deploy com Docker
- **Testes automatizados** e TDD
- **Frontend responsivo** sem frameworks

## 👤 Desenvolvedor

**Douglas** - [@notdougz](https://github.com/notdougz)

_Projeto desenvolvido como parte do meu aprendizado em desenvolvimento full-stack_

---

⭐ **Gostou do projeto?** Deixe uma estrela para apoiar meu aprendizado!
