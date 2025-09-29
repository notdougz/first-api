# API de Gerenciamento de Tarefas com FastAPI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)

## 📝 Descrição do Projeto

Este projeto é uma API RESTful desenvolvida em Python com o framework FastAPI. A aplicação permite o gerenciamento completo de uma lista de tarefas (To-Do list), com funcionalidades para criar, ler, atualizar e deletar tarefas (operações CRUD).

O projeto evoluiu de um sistema em memória para uma aplicação com **persistência de dados em banco SQLite**, utilizando **SQLAlchemy** com suporte assíncrono para melhor performance. Foi desenvolvido como um projeto de estudo para solidificar conceitos de desenvolvimento backend, construção de APIs RESTful, programação assíncrona e boas práticas de arquitetura de software.

## ✨ Funcionalidades

### Implementadas ✅
- **Criar** uma nova tarefa com título, descrição e status
- **Listar** todas as tarefas existentes com paginação
- **Persistência de dados** em banco de dados SQLite
- Validação automática de dados de entrada com **Pydantic**
- Documentação interativa e automática da API com **Swagger UI**
- Arquitetura modular e organizada (separação de responsabilidades)
- Operações assíncronas para melhor performance

### Em Desenvolvimento 🚧
- **Obter** uma tarefa específica por seu ID
- **Atualizar** uma tarefa existente (título, descrição, status)
- **Deletar** uma tarefa
- Filtros e busca de tarefas

## 🏗️ Arquitetura do Projeto

```
projeto-tarefas/
│
├── main.py          # Aplicação principal e definição dos endpoints
├── database.py      # Configuração e conexão com o banco de dados
├── models.py        # Modelos SQLAlchemy (representação das tabelas)
├── schemas.py       # Esquemas Pydantic (validação de dados)
├── crud.py          # Operações CRUD no banco de dados
├── requirements.txt # Dependências do projeto
├── tarefas.db      # Banco de dados SQLite (criado automaticamente)
└── README.md       # Documentação do projeto
```

## 💻 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação principal
- **FastAPI**: Framework web moderno, rápido e com tipagem
- **SQLAlchemy 2.0**: ORM para interação com banco de dados
- **SQLite**: Banco de dados leve e sem necessidade de servidor
- **Aiosqlite**: Driver assíncrono para SQLite
- **Uvicorn**: Servidor ASGI para executar a aplicação
- **Pydantic**: Validação e serialização de dados

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

### Pré-requisitos
- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

### Passo a Passo

**1. Clone o repositório:**
```bash
git clone https://github.com/notdougz/first-api.git
cd first-api/projeto-tarefas
```

**2. Crie e ative o ambiente virtual:**

* **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
* **Linux / macOS:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

**3. Instale as dependências:**
```bash
pip install fastapi uvicorn sqlalchemy aiosqlite
```

Ou se você tiver um arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

**4. Execute a API:**
```bash
uvicorn main:app --reload
```

> 💡 **Nota:** O banco de dados SQLite (`tarefas.db`) será criado automaticamente na primeira execução da aplicação.

**5. Acesse a aplicação:**
- API: `http://127.0.0.1:8000`
- Documentação interativa (Swagger): `http://127.0.0.1:8000/docs`
- Documentação alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

## 📚 Documentação da API

### Endpoints Disponíveis

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| `GET` | `/` | Retorna mensagem de boas-vindas | ✅ Implementado |
| `POST` | `/tarefas/` | Cria uma nova tarefa | ✅ Implementado |
| `GET` | `/tarefas/` | Lista todas as tarefas | ✅ Implementado |
| `GET` | `/tarefas/{id}` | Obtém uma tarefa específica | 🚧 Em desenvolvimento |
| `PUT` | `/tarefas/{id}` | Atualiza uma tarefa | 🚧 Em desenvolvimento |
| `DELETE` | `/tarefas/{id}` | Deleta uma tarefa | 🚧 Em desenvolvimento |

### Exemplos de Uso

#### Criar uma nova tarefa
```bash
curl -X POST "http://127.0.0.1:8000/tarefas/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Estudar FastAPI",
    "descricao": "Completar o tutorial oficial",
    "concluida": false
  }'
```

#### Listar todas as tarefas
```bash
curl -X GET "http://127.0.0.1:8000/tarefas/"
```

### Estrutura dos Dados

#### Modelo de Tarefa
```json
{
  "id": 1,
  "titulo": "string",
  "descricao": "string (opcional)",
  "concluida": false
}
```

## 🔄 Fluxo de Dados

1. **Cliente** envia requisição HTTP para a API
2. **FastAPI** valida os dados usando os **Schemas (Pydantic)**
3. **CRUD Operations** processa a lógica de negócio
4. **SQLAlchemy** traduz as operações para SQL
5. **SQLite** persiste/recupera os dados
6. **API** retorna a resposta formatada ao cliente

## 📈 Próximos Passos e Melhorias

### Curto Prazo
- [ ] Implementar endpoints de UPDATE e DELETE
- [ ] Adicionar endpoint para buscar tarefa por ID
- [ ] Implementar filtros (tarefas concluídas/pendentes)
- [ ] Adicionar campo de data de criação e atualização

### Médio Prazo
- [ ] Implementar autenticação e autorização (OAuth2/JWT)
- [ ] Adicionar sistema de usuários
- [ ] Implementar categorias/tags para tarefas
- [ ] Adicionar prioridade nas tarefas
- [ ] Criar testes unitários e de integração

### Longo Prazo
- [ ] Migrar para PostgreSQL para produção
- [ ] Implementar cache com Redis
- [ ] Adicionar sistema de notificações
- [ ] Criar interface web (Frontend)
- [ ] Deploy em serviço de cloud (AWS/Heroku/Railway)
- [ ] Implementar CI/CD com GitHub Actions

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Se você tem alguma sugestão ou encontrou um bug:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## 👤 Autor

**Douglas** - [@notdougz](https://github.com/notdougz)

---

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!