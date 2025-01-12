# Imagem base do Node.js para build
FROM node:18 AS build-stage

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar arquivos do projeto para o container
COPY package*.json ./
COPY . .

# Instalar dependências e gerar build
RUN npm install
RUN npm run build

# Imagem base do Nginx para servir os arquivos estáticos
FROM nginx:1.21 AS production-stage

# Copiar o build para o diretório do Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copiar configuração customizada do Nginx (opcional)
COPY nginx.conf /etc/nginx/nginx.conf

# Expor porta do Nginx
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
