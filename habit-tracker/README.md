# Habit Tracker

A small FastAPI service for tracking daily habits and calculating streaks, backed by PostgreSQL.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/habits` | Create a new habit (`{"name": "..."}`) |
| GET | `/habits` | List all habits |
| POST | `/habits/{habit_id}/complete` | Mark a habit completed for today |
| GET | `/habits/{habit_id}/streak` | Get the current streak (longest run of consecutive completed days) for a habit |

Interactive docs available at `/docs` once running.

## Run locally with Docker Compose (recommended)

This starts both the API and its PostgreSQL database, correctly networked together.

```bash
git clone https://github.com/mabelbyband-star/Backend-microservices-portfolio.git
cd Backend-microservices-portfolio/habit-tracker
docker compose up -d
```

The API will be available at `http://localhost:8000`.

To stop:
```bash
docker compose down
```

Data persists across restarts (`docker compose down` followed by `up` again) thanks to a named volume. To wipe all data too:
```bash
docker compose down -v
```

## Run with a pre-built image from Docker Hub

```bash
docker pull erhb/habit-tracker
```

Note: the app expects a PostgreSQL database reachable at host `db` (or set the `DB_HOST` environment variable to point elsewhere). Running the image alone, without a database, will start the server but any endpoint touching the database will fail. Use the Docker Compose method above for a fully working setup.

## Running tests

```bash
cd habit-tracker
pip install -r requirements.txt
docker compose up -d db
DB_HOST=localhost pytest
```

## Stack

Python 3.12 · FastAPI · PostgreSQL 16 · Docker Compose · GitHub Actions (CI/CD)
