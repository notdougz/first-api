# API de Gerenciamento de Tarefas com FastAPI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=for-the-badge&logo=fastapi)

## 📝 Descrição do Projeto

Este projeto é uma API RESTful desenvolvida em Python com o framework FastAPI. A aplicação permite o gerenciamento completo de uma lista de tarefas (To-Do list), com funcionalidades para criar, ler, atualizar e deletar tarefas (operações CRUD).

Foi criado como um projeto de estudo para solidificar conceitos de desenvolvimento backend, construção de APIs e boas práticas de programação.

## ✨ Funcionalidades

- **Criar** uma nova tarefa
- **Listar** todas as tarefas existentes
- **Obter** uma tarefa específica por seu ID
- **Atualizar** uma tarefa existente (título, descrição, status)
- **Deletar** uma tarefa
- Validação de dados de entrada com **Pydantic**
- Documentação interativa e automática da API com **Swagger UI**

## 💻 Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI**: Framework web moderno e de alta performance.
- **Uvicorn**: Servidor ASGI para executar a aplicação.
- **Pydantic**: Para validação e configuração de modelos de dados.

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clone o repositório:**
```bash
git clone [https://github.com/notdougz/first-api.git](https://github.com/notdougz/first-api.git)
```

**2. Acesse a pasta do projeto:**
```bash
cd first-api
```

**3. Crie e ative o ambiente virtual:**

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

**4. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**5. Execute a API:**
```bash
uvicorn main:app --reload
```
O servidor estará rodando e a opção `--reload` fará com que ele reinicie automaticamente a cada alteração no código.

**6. Acesse em seu navegador:**
A aplicação estará disponível em `http://127.0.0.1:8000`.

## 🛠️ Como Usar (Endpoints da API)

A forma mais fácil de interagir e testar a API é através da documentação interativa (Swagger UI), que é gerada automaticamente pelo FastAPI.

Acesse o seguinte endereço no seu navegador após iniciar o servidor:
**`http://127.0.0.1:8000/docs`**

Lá, você poderá ver todos os endpoints disponíveis e testá-los diretamente.

### Resumo dos Endpoints

| Método HTTP | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/tarefas/` | Cria uma nova tarefa. |
| `GET` | `/tarefas/` | Lista todas as tarefas existentes. |
| `GET` | `/tarefas/{tarefa_id}` | Obtém uma tarefa específica pelo seu ID. |
| `PUT` | `/tarefas/{tarefa_id}` | Atualiza uma tarefa existente pelo seu ID. |
| `DELETE` | `/tarefas/{tarefa_id}` | Deleta uma tarefa pelo seu ID. |

## 📈 Próximos Passos (Melhorias Futuras)

- [ ] Integração com um banco de dados (SQLite ou PostgreSQL) para persistência dos dados.
- [ ] Adicionar um sistema de autenticação de usuários (ex: OAuth2 com JWT).
- [ ] Escrever testes unitários e de integração para garantir a qualidade e estabilidade do código.
- [ ] Realizar o deploy da aplicação em um serviço de nuvem (ex: Heroku, AWS, etc.).

---
