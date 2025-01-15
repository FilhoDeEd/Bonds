FROM node:20

WORKDIR /app/frontend

COPY frontend/package*.json .

COPY frontend/ /app/frontend/

COPY entrypoint.frontend.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
