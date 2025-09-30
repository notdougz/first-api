# API de Gerenciamento de Tarefas com FastAPI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge)

## 📝 Descrição do Projeto

Este projeto é uma API RESTful desenvolvida em Python com o framework FastAPI. A aplicação permite o gerenciamento completo de uma lista de tarefas (To-Do list), com funcionalidades para criar, ler, atualizar e deletar tarefas (operações CRUD), além de um **sistema completo de autenticação e autorização** com JWT.

O projeto evoluiu de um sistema em memória para uma aplicação robusta com **persistência de dados em banco SQLite**, utilizando **SQLAlchemy** com suporte assíncrono para melhor performance. Cada usuário possui suas próprias tarefas privadas, garantindo segurança e isolamento de dados.

Foi desenvolvido como um projeto de estudo para solidificar conceitos de desenvolvimento backend, construção de APIs RESTful, segurança, autenticação, programação assíncrona e boas práticas de arquitetura de software.

## ✨ Funcionalidades

### Implementadas ✅
- **Sistema de Autenticação Completo**
  - Registro de novos usuários com senha criptografada (bcrypt)
  - Login com geração de token JWT
  - Proteção de rotas com verificação de token
  - Cada usuário acessa apenas suas próprias tarefas
- **Gerenciamento de Tarefas**
  - Criar uma nova tarefa (privada para o usuário)
  - Listar todas as tarefas do usuário autenticado
  - Obter uma tarefa específica por ID
  - Atualizar uma tarefa existente
  - Deletar uma tarefa
- **Persistência de dados** em banco de dados SQLite
- **Relacionamento entre tabelas** (Usuários ↔ Tarefas)
- Validação automática de dados de entrada com **Pydantic**
- Documentação interativa e automática da API com **Swagger UI**
- Arquitetura modular e organizada (separação de responsabilidades)
- Operações assíncronas para melhor performance
- Paginação de resultados

### Em Desenvolvimento 🚧
- Filtros e busca avançada de tarefas
- Sistema de categorias/tags
- Prioridades nas tarefas
- Datas de vencimento

## 🏗️ Arquitetura do Projeto

```
projeto-tarefas/
│
├── main.py          # Aplicação principal e definição dos endpoints
├── database.py      # Configuração e conexão com o banco de dados
├── models.py        # Modelos SQLAlchemy (representação das tabelas)
├── schemas.py       # Esquemas Pydantic (validação de dados)
├── crud.py          # Operações CRUD no banco de dados
├── auth.py          # Lógica de autenticação e segurança (JWT)
├── .env             # Variáveis de ambiente (SECRET_KEY, etc)
├── .gitignore       # Arquivos ignorados pelo Git
├── requirements.txt # Dependências do projeto
├── tarefas.db       # Banco de dados SQLite (criado automaticamente)
└── README.md        # Documentação do projeto
```

## 💻 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação principal
- **FastAPI**: Framework web moderno, rápido e com tipagem
- **SQLAlchemy 2.0**: ORM para interação com banco de dados
- **SQLite**: Banco de dados leve e sem necessidade de servidor
- **Aiosqlite**: Driver assíncrono para SQLite
- **Uvicorn**: Servidor ASGI para executar a aplicação
- **Pydantic**: Validação e serialização de dados
- **python-jose[cryptography]**: Criação e validação de tokens JWT
- **passlib[bcrypt]**: Hash seguro de senhas
- **python-multipart**: Suporte para formulários OAuth2
- **python-dotenv**: Gerenciamento de variáveis de ambiente

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
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```
* **Linux / macOS:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

**3. Instale as dependências:**
```bash
pip install fastapi uvicorn sqlalchemy aiosqlite python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv
```

Ou se você tiver um arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```env
SECRET_KEY=sua_chave_secreta_super_segura_aqui_com_pelo_menos_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **IMPORTANTE:** Gere uma SECRET_KEY segura! Você pode usar o comando abaixo:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**5. Execute a API:**
```bash
uvicorn main:app --reload
```

> 💡 **Nota:** O banco de dados SQLite (`tarefas.db`) será criado automaticamente na primeira execução da aplicação.

**6. Acesse a aplicação:**
- API: `http://127.0.0.1:8000`
- Documentação interativa (Swagger): `http://127.0.0.1:8000/docs`
- Documentação alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

## 📚 Documentação da API

### Endpoints Disponíveis

| Método | Endpoint | Descrição | Autenticação | Status |
|--------|----------|-----------|--------------|--------|
| `GET` | `/` | Retorna mensagem de boas-vindas | ❌ Não | ✅ Implementado |
| `POST` | `/usuarios/` | Registra um novo usuário | ❌ Não | ✅ Implementado |
| `POST` | `/login` | Autentica e retorna token JWT | ❌ Não | ✅ Implementado |
| `POST` | `/tarefas/` | Cria uma nova tarefa | ✅ Sim | ✅ Implementado |
| `GET` | `/tarefas/` | Lista tarefas do usuário | ✅ Sim | ✅ Implementado |
| `GET` | `/tarefas/{id}` | Obtém uma tarefa específica | ✅ Sim | ✅ Implementado |
| `PUT` | `/tarefas/{id}` | Atualiza uma tarefa | ✅ Sim | ✅ Implementado |
| `DELETE` | `/tarefas/{id}` | Deleta uma tarefa | ✅ Sim | ✅ Implementado |

### Exemplos de Uso

#### 1. Registrar um novo usuário
```bash
curl -X POST "http://127.0.0.1:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "senha": "senha_segura_123"
  }'
```

#### 2. Fazer login e obter token
```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@exemplo.com&password=senha_segura_123"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Criar uma nova tarefa (autenticado)
```bash
curl -X POST "http://127.0.0.1:8000/tarefas/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "titulo": "Estudar FastAPI",
    "descricao": "Completar o tutorial oficial",
    "concluida": false
  }'
```

#### 4. Listar todas as tarefas do usuário
```bash
curl -X GET "http://127.0.0.1:8000/tarefas/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### 5. Atualizar uma tarefa
```bash
curl -X PUT "http://127.0.0.1:8000/tarefas/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "titulo": "Estudar FastAPI - Atualizado",
    "descricao": "Tutorial completo",
    "concluida": true
  }'
```

#### 6. Deletar uma tarefa
```bash
curl -X DELETE "http://127.0.0.1:8000/tarefas/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Estrutura dos Dados

#### Modelo de Usuário
```json
{
  "id": 1,
  "email": "usuario@exemplo.com"
}
```

#### Modelo de Tarefa
```json
{
  "id": 1,
  "titulo": "string",
  "descricao": "string (opcional)",
  "concluida": false,
  "dono_id": 1
}
```

#### Token de Acesso
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 🔄 Fluxo de Dados e Autenticação

### Fluxo de Registro e Login
1. **Usuário** envia credenciais (email e senha)
2. **API** valida os dados com Pydantic
3. **Senha** é criptografada com bcrypt
4. **Usuário** é salvo no banco de dados
5. No login, **JWT token** é gerado e retornado

### Fluxo de Requisições Protegidas
1. **Cliente** envia requisição com token JWT no header Authorization
2. **FastAPI** intercepta e valida o token (auth.py)
3. Se válido, **usuário é identificado** e recuperado do banco
4. **CRUD Operations** processa a lógica com contexto do usuário
5. **SQLAlchemy** executa operações apenas nos dados do usuário
6. **API** retorna a resposta formatada

## 🔒 Segurança

### Implementações de Segurança
- ✅ **Senhas criptografadas** com bcrypt (nunca armazenadas em texto puro)
- ✅ **Autenticação JWT** com tokens de acesso
- ✅ **Tokens com expiração** configurável
- ✅ **Isolamento de dados** por usuário
- ✅ **Validação de propriedade** (usuários só acessam suas tarefas)
- ✅ **SECRET_KEY em variável de ambiente**
- ✅ **Proteção contra SQL Injection** (uso de ORM)

### Boas Práticas Implementadas
- Arquivo `.env` para segredos (não versionado)
- Validação de dados com Pydantic
- Tratamento de erros apropriado
- Status codes HTTP corretos
- Documentação automática da API

## 📈 Próximos Passos e Melhorias

### Curto Prazo
- [ ] Implementar refresh tokens
- [ ] Adicionar campo de data de criação e atualização nas tarefas
- [ ] Implementar filtros (tarefas concluídas/pendentes)
- [ ] Adicionar busca por título/descrição
- [ ] Limitar tamanho de título e descrição

### Médio Prazo
- [ ] Implementar categorias/tags para tarefas
- [ ] Adicionar prioridade nas tarefas (alta, média, baixa)
- [ ] Sistema de datas de vencimento com lembretes
- [ ] Criar testes unitários e de integração
- [ ] Implementar rate limiting
- [ ] Adicionar logs estruturados

### Longo Prazo
- [ ] Migrar para PostgreSQL para produção
- [ ] Implementar cache com Redis
- [ ] Adicionar sistema de notificações (email/push)
- [ ] Criar interface web (Frontend em React/Vue)
- [ ] Implementar compartilhamento de tarefas entre usuários
- [ ] Deploy em serviço de cloud (AWS/Heroku/Railway)
- [ ] Implementar CI/CD com GitHub Actions
- [ ] Adicionar suporte a anexos/arquivos
- [ ] Sistema de backup automático

## 🧪 Testando a API

### Usando o Swagger UI
1. Acesse `http://127.0.0.1:8000/docs`
2. Clique em "POST /usuarios/" para registrar
3. Clique em "POST /login" para obter o token
4. Clique no botão "Authorize" no topo da página
5. Cole o token (apenas o token, sem "Bearer")
6. Agora você pode testar todos os endpoints protegidos!

### Usando o Postman/Insomnia
1. Crie uma requisição POST para `/usuarios/`
2. Faça login em POST `/login`
3. Copie o `access_token` da resposta
4. Nas próximas requisições, adicione o header:
   ```
   Authorization: Bearer SEU_TOKEN_AQUI
   ```

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Se você tem alguma sugestão ou encontrou um bug:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Notas de Desenvolvimento

### Estrutura do Banco de Dados
O projeto usa SQLite com duas tabelas relacionadas:
- **usuarios**: Armazena os usuários do sistema
- **tarefas**: Armazena as tarefas, cada uma vinculada a um usuário através de `dono_id`

### Ambiente Virtual
O projeto usa `.venv` como ambiente virtual. Certifique-se de ativá-lo antes de trabalhar no projeto.

### Variáveis de Ambiente
Nunca commite o arquivo `.env` para o repositório. Ele está incluído no `.gitignore` por questões de segurança.

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## 👤 Autor

**Douglas** - [@notdougz](https://github.com/notdougz)

---

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!

## 📚 Recursos de Aprendizagem

- [Documentação oficial do FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial de JWT](https://jwt.io/introduction)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Boas práticas de segurança em APIs](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)