# Development Guide

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [GNU Make](https://www.gnu.org/software/make/)
- [pre-commit](https://pre-commit.com/#install) for code quality checks (optional)

### 1. Clone the repository

```bash
git clone https://github.com/teenxsky/money-flow.git
cd money-flow
```

### 2. Set up environment variables

Create local environment files based on the examples:

```bash
cd deployments/dev/conf
cp .env.docker .env.docker.local
cp .env.backend .env.backend.local
```

Fill in the required fields in newly created `.env.docker.local` and `.env.backend.local` files.

### 3. Set up pre-commit hooks (optional)

Pre-commit ensures code quality and formatting before each commit.

```bash
pre-commit install
```

### 4. Build and start the development environment

From the project root:

```bash
make build-dev
make up-dev # or make up-logs-dev
```

This will start:
- Nginx web server
- Django backend
- PostgreSQL database
- Frontend

Also local folders with modules will be created:
- /backend/**.venv/**
- /frontend/**node_modules/**

### 4.1. Apply database migrations and load reference data

After the containers are up, apply Django migrations and load reference data:

```bash
make migrate-dev
make load-reference-data-dev
```

- `make migrate-dev` — applies all pending Django migrations to the development database.
- `make load-reference-data-dev` — loads initial reference data required for application to function properly.

### 5. Access the application

The application will be available at:

- Frontend: http://localhost:80/
- Backend API: http://api.localhost:80/
- Backend docs (Swagger UI): http://api.localhost:80/v1/docs/
- Backend admin panel: http://api.localhost:80/admin

### 6*. Common Development Commands (Additional info)

### Docker

- **Up containers with logs:**  
  ```bash
  make up-logs-dev
  ```
- **Up containers without logs:**  
  ```bash
  make up-dev
  ```
- **Build images:**  
  ```bash
  make build-dev
  ```
- **Stop containers:**  
  ```bash
  make down-dev
  ```
- **Restart contaiers:**  
  ```bash
  make restart-dev
  ```
- **Clean images:**  
  ```bash
  make clean-dev
  ```
- **Clean volumes:**  
  ```bash
  make clean-volumes-dev
  ```

### Backend (Django)

- **Run django tests:**  
  ```bash
  make run-tests-dev
  ```
- **Create a Django app:**  
  ```bash
  make startapp-dev
  ```
- **Create a Django admin:**  
  ```bash
  make createsuperuser-dev
  ```
- **Make Django migrations:**  
  ```bash
  make makemigrations-dev
  ```
- **Run Django migrations:**  
  ```bash
  make migrate-dev
  ```
- **Add a backend dependency (package):**  
  ```bash
  make add-back-dep
  ```
- **Add a backend dependency (package) for developmet:**  
  ```bash
  make add-back-dep-dev
  ```
- **Remove a backend dependency (package):**  
  ```bash
  remove-back-dep
  ```
- **Format backend code:**  
  ```bash
  make run-back-format
  ```
- **Lint backend code:**  
  ```bash
  make run-back-lint
  ```

### Frontend (Node.js)

- **Add a frontend dependency (package):**  
  ```bash
  make add-front-dep
  ```
- **Add a frontend dependency (package) for developmet:**  
  ```bash
  make add-front-dep-dev
  ```
- **Remove a frontend dependency (package):**  
  ```bash
  make remove-front-dep
  ```
- **Format frontend code:**  
  ```bash
  make run-front-format
  ```
- **Run frontend linting:**  
  ```bash
  make run-front-lint
  ```

See the `Makefile` for more commands and details. For get details use command:
```bash
make help
```
