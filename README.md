# tourtoise Agent API

Tourtoise Agent API is a backend service designed for an AI-powered tour assistant.
It helps user to plan their tour, suggests locations, what activitis to do, track 
user's location with their permission and suggest as a tour guide.

---

## Features

* AI-powered tour assistant
* Plan tours for users
* Find destinations for users, plan budget and other iteneris
* Adjust tour plan according to weather and other variables

---

## Tech Stack

* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy + Alembic**
* **Celery**
* **Redis**
* **Docker**
* **Google ADK**
* **Vertex AI**
* **Confluent**


---

## Running the Project

### **1. Docker (Recommended)**

For Linux and macOS:

```bash
./startapp.sh
```

This script will:

* build images
* start PostgreSQL, Redis, the API server, and Celery workers
* run health checks
* prepare the environment

After startup, API is available at:

```
http://localhost:5000
```

---

### **2. Manual Installation (Without Docker)**

#### **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### **Install dependencies**

```bash
pip install -r requirements.txt
```

#### **Start the required services**

You must run these individually:

* PostgreSQL (database)
* Redis (Celery broker)
* Celery worker
* FastAPI app

Example:

```bash
uvicorn app.main:app --reload --port 5000
celery -A app.core.celery.celery_app worker --loglevel=info
```

Make sure PostgreSQL credentials match your `.env` file.

---

## Database Migrations (Alembic)

Alembic is already set up in the project.

To apply all migrations:

```bash
alembic upgrade head
```

To create a new migration after updating models:

```bash
alembic revision --autogenerate -m "your message"
```

---

## Environment Variables

Create a `.env` file at the root following `.env.example`

---

## Project Structure

```
app/
│── api/              # API routes
│── base/             # Base models and schema
│── core/             # config, celery, logging
│── db/               # database session, models
│── middleware/       # Middlewares and Exception Handlers
│── main.py           # FastAPI entrypoint
alembic/              # migration directory
.env
docker-compose.yml
Dockerfile
startapp.sh
README.md
```

---

## API Documentation

FastAPI automatically generates docs:

Swagger UI:

```
http://localhost:5000/api/v1/docs
```

ReDoc:

```
http://localhost:5000/api/v1/redoc
```
git remote add origin https://github.com/shahtaz-tqldd/tourtoise-agent-api.git