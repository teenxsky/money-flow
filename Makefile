COMPOSE_DEV = docker-compose -f ./deployments/dev/docker-compose.yaml \
			--env-file=./deployments/dev/conf/.env.docker.local


.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' \
	$(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


#--------------- DOCKER COMPOSE COMMANDS ---------------#

.PHONY: build-dev
build-dev: ## Build the Docker images for the development environment
	@$(COMPOSE_DEV) build

.PHONY: up-dev
up-dev: ## Start the development environment
	@$(COMPOSE_DEV) up -d

.PHONY: up-logs-dev
up-logs-dev: ## Start the development environment and display logs
	@$(COMPOSE_DEV) up

.PHONY: down-dev
down-dev: ## Stop the development environment
	@$(COMPOSE_DEV) down

.PHONY: clean-dev
clean-dev: ## Clean up the development environment
	@$(COMPOSE_DEV) down --rmi all

.PHONY: clean-volumes-dev
clean-volumes-dev: ## Clean up the development environment volumes
	@$(COMPOSE_DEV) down -v

.PHONY: restart-dev
restart-dev: ## Restart the development environment
	@$(COMPOSE_DEV) restart


#--------------- DJANGO COMMANDS ---------------#

.PHONY: add-dependency
add-dependency: ## Add dependency to stage environment
	@sh -c 'read -p "Enter the dependency name: " dep_name && \
	echo "Installing dependency: $$dep_name" && \
	$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry add $$dep_name"'

.PHONY: add-dependency-dev
add-dependency-dev: ## Add dependency to the development environment
	@sh -c 'read -p "Enter the dependency name for development: " dep_name && \
	echo "Installing dependency: $$dep_name" && \
	$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry add $$dep_name --dev"'

.PHONY: remove-dependency
remove-dependency: ## Remove dependency from stage environment
	@sh -c 'read -p "Enter the dependency name: " dep_name && \
	echo "Removing dependency: $$dep_name" && \
	$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry remove $$dep_name"'

.PHONY: remove-dependency-dev
remove-dependency-dev: ## Remove dependency from the development environment
	@sh -c 'read -p "Enter the dependency name for development: " dep_name && \
	echo "Removing dependency: $$dep_name" && \
	$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry remove $$dep_name --dev"'

.PHONY: migrate-dev
migrate-dev: ## Run Django migrations for the development environment
	@$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry run python manage.py migrate"

.PHONY: makemigrations-dev
makemigrations-dev: ## Make migrations for the development environment
	@$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry run python manage.py makemigrations"

.PHONY: startapp-dev
startapp-dev: ## Create a new Django app in the development environment
	@sh -c 'read -p "Enter the django app name: " dep_name && \
	echo "Creating Django app: $$dep_name" && \
	$(COMPOSE_DEV) exec backend sh -c \
	"cd src/apps && poetry run python ../manage.py startapp $$dep_name"'

.PHONY: createsuperuser-dev
createsuperuser-dev: ## Create a superuser in the development environment
	@$(COMPOSE_DEV) exec backend sh -c \
	"cd src && poetry run python manage.py createsuperuser"


#--------------- LINT/FORMAT COMMANDS ---------------#


.PHONY: run-lint
run-lint: ## Run linting for the development environment
	@$(COMPOSE_DEV) exec backend sh -c \
	"poetry run ruff check --config=ruff.toml"

.PHONY: run-formatter
run-formatter: ## Format code for the development environment
	@$(COMPOSE_DEV) exec backend sh -c \
	"poetry run ruff format --config=ruff.toml"
