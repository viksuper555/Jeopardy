# Trivia Application

## Overview
A trivia application with database integration, API endpoints, and dataset management.

## Requirements
- Python 3.12
- PostgreSQL
- Docker (optional for containerized deployment)

## Setup

### Installing Dependencies
```powershell
pip install -r requirements.txt
```

### Database Configuration
1. Make sure PostgreSQL is running
2. Configure database connection in the `.env` file
3. Run database migrations:
```powershell
alembic upgrade head
```

## Database Migrations with Alembic

The project uses Alembic for database schema migrations. Here are common operations:

### Configuration

Alembic is configured through:
- `alembic.ini`: Main configuration file 
- `alembic/env.py`: Environment configuration that connects to the database
- `.env`: Contains database credentials used by Alembic

The database connection string is automatically generated from environment variables:
```
DB_HOST=localhost
DB_USER=postgres
DB_PASS=your_password
DB_NAME=jeopardy
DB_PORT=5432
```

### Migration Commands

#### Creating a New Migration
To create a new migration after model changes:

```powershell
# Auto-generate migration based on model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration file
alembic revision -m "Description of changes"
```

#### Applying Migrations

```powershell
# Apply all migrations up to the latest
alembic upgrade head

# Apply next migration
alembic upgrade +1

# Apply specific migration by ID
alembic upgrade revision_id

# Rollback last migration
alembic downgrade -1

# Rollback to a specific revision
alembic downgrade revision_id
```

#### Migration Information

```powershell
# View current migration version
alembic current

# View migration history
alembic history --verbose
```

### Loading Dataset
```powershell
python app/dataset_loader.py --verbose
```

## Running the Application

### Development Mode
```powershell
uvicorn app.main:app --reload
```

### Docker Deployment
```powershell
docker-compose up -d
```

#### OpenAI API Key Configuration
The application requires an OpenAI API key for certain functionality. When using Docker Compose:

1. The key is defined in the `docker-compose.yml` file in the `environment` section
2. You can change it by editing the file directly or by setting an environment variable:

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
docker-compose up -d
```

Alternatively, you can create/edit a `.env` file in the project root with:
```
OPENAI_API_KEY=your-api-key-here
```

## Project Structure
- `app/`: Main application code
- `alembic/`: Database migration scripts
- `Dockerfile` & `docker-compose.yml`: Container configuration