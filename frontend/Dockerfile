# --- Estágio 1: Build ---
# Usamos uma imagem base leve para o Nginx.
FROM nginx:1.25-alpine

# Remove a configuração padrão do Nginx.
RUN rm /etc/nginx/conf.d/default.conf

# Copia a nossa configuração personalizada para o Nginx.
COPY nginx.conf /etc/nginx/conf.d/

# Copia os arquivos do nosso front-end (HTML, CSS, JS) para a pasta
# que o Nginx usa para servir sites.
COPY . /usr/share/nginx/html

# Expõe a porta 80, que é a porta padrão para tráfego web (HTTP).
EXPOSE 80

# O comando para iniciar o servidor Nginx.
CMD ["nginx", "-g", "daemon off;"]