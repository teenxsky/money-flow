# Money Flow

Money Flow is a financial management application that helps you track income, expenses, and manage your personal or business finances. It consists of a Django backend API, a web frontend, and is containerized with Docker for easy deployment.

## Project Structure

- `backend/` - Django backend API
- `frontend/` - Frontend application (to be implemented)
- `deployments/` - Docker configuration for development and production environments

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) 3.13 or higher
- [pre-commit](https://pre-commit.com/#install) for code quality checks
- [Git](https://git-scm.com/downloads)

## Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd money-flow
```

### 2. Set up environment variables

Create local environment files based on the examples:

```bash
# Create environment file for development environment
cd deployments/dev/conf
cp .env.docker .env.docker.local
cp .env.backend .env.backend.local
```

Be sure to fill in the missing fields in the resulting files.

### 3. Set up pre-commit

Install pre-commit hooks:

```bash
cd backend
pre-commit install
```

### 4. Start the development environment with Docker

```bash
cd money-flow
make dev-up
```

This will start:

- Nginx web server
- Django backend
- PostgreSQL database

### 5. Access the application

The application will be available at:

- Backend API: http://api.localhost:80/
- Admin panel: http://api.localhost:80/admin

## Common Development Commands

```bash
# Start the development environment
make up-dev

# Stop the development environment
make down-dev
```

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
