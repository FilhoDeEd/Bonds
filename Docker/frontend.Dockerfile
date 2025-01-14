FROM node:20

WORKDIR /app

COPY frontend/package*.json .

RUN npm install

COPY frontend/ .

COPY entrypoint.frontend.sh /app/
RUN chmod +x /app/entrypoint.frontend.sh

ENTRYPOINT ["/app/entrypoint.frontend.sh"]
