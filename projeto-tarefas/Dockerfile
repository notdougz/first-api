# Versão do Python: Python 3.11 slim, uma imagem leve e otimizada.
FROM python:3.11-slim

# 2. Diretório de Trabalho: Define o diretório padrão dentro do container.
#    Todos os comandos a seguir serão executados a partir de /app.
WORKDIR /app

# 3. Copiar e Instalar Dependências:
#    Copiamos primeiro o requirements.txt para aproveitar o cache do Docker.
#    Se não mudarmos as dependências, o Docker não precisa reinstalar tudo.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o Código da Aplicação:
COPY . .

# 5. Expor a Porta:
#    Informa ao Docker que a nossa aplicação vai "escutar" na porta 8000.
EXPOSE 8000

# 6. Comando de Execução:
#    Este é o comando que será executado quando o container iniciar.
#    O host '0.0.0.0' é crucial para que a API seja acessível de fora do container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]