FROM node:20

WORKDIR /app

COPY frontend/package*.json .

RUN npm install

COPY api.js /
COPY frontend/ .

RUN npm run build
