FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY backend/ /app/backend/

COPY entrypoint.backend.sh /app/
RUN chmod +x /app/entrypoint.backend.sh

ENTRYPOINT ["/app/entrypoint.backend.sh"]
