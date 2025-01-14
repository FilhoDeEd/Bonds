DOCKER_COMPOSE_FILE = docker-compose-production.yml
DOCKER_COMPOSE_ENV_FILE = env/production.env

.PHONY: build_frontend build_up up down

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
