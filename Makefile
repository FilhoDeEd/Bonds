DOCKER_COMPOSE_FILE = docker-compose-production.yml
DOCKER_COMPOSE_ENV_FILE = env/production.env
BACKEND_CONTAINER_NAME = backend_production

.PHONY: build_frontend build_up up down import_neighborhoods create_forums check_backend

check_backend:
	@docker inspect -f '{{.State.Running}}' $(BACKEND_CONTAINER_NAME) 2>/dev/null | grep -q true || (echo "Backend container is not running. Start it first with 'make up'." && exit 1)

build_frontend:
	@echo "Building frontend..."
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile build --env-file $(DOCKER_COMPOSE_ENV_FILE) up --build
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile build --env-file $(DOCKER_COMPOSE_ENV_FILE) rm -f frontend

build_up:
	@echo "Building and starting all services..."
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile run --env-file $(DOCKER_COMPOSE_ENV_FILE) up --build -d

up:
	@echo "Starting all services..."
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile run --env-file $(DOCKER_COMPOSE_ENV_FILE) up -d

down:
	@echo "Stopping all services..."
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile run --env-file $(DOCKER_COMPOSE_ENV_FILE) down

import_neighborhoods: check_backend
	@echo "Importing neighborhoods..."
	docker exec -it $(BACKEND_CONTAINER_NAME) python manage.py import_neighborhoods

create_forums: check_backend
	@echo "Creating default forums..."
	docker exec -it $(BACKEND_CONTAINER_NAME) python manage.py create_default_forums
