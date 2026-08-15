# Vehicle Customizer

An interactive command-line app for building a custom vehicle (brand, model, color, upgrades), with each build saved to PostgreSQL. Includes a companion FastAPI service for viewing saved vehicles over HTTP.

This project runs as two separate services from the same codebase: an interactive script (`app`) and a web API (`api`), both sharing one PostgreSQL database (`db`).

## Endpoints (API service)

| Method | Path | Description |
|---|---|---|
| GET | `/vehicles` | List all saved vehicles |

Interactive docs available at `/docs` once running.

## Run locally with Docker Compose (recommended)

This starts all three services together, correctly networked: the interactive builder, the API, and the database.

```bash
git clone https://github.com/mabelbyband-star/Backend-microservices-portfolio.git
cd Backend-microservices-portfolio/vehicle-db-app
docker compose up -d
```

The API will be available at `http://localhost:8000`.

To use the interactive vehicle builder directly (typed input required):
```bash
docker compose run app
```

To stop everything:
```bash
docker compose down
```

Data persists across restarts (`docker compose down` followed by `up` again) thanks to a named volume. To wipe all data too:
```bash
docker compose down -v
```

## Run with a pre-built image from Docker Hub

```bash
docker pull erhb/vehicle-db-app
```

Note: the app expects a PostgreSQL database reachable at host `db` (or set the `DB_HOST` environment variable to point elsewhere). Running the image alone, without a database, will start the server but any endpoint touching the database will fail. Use the Docker Compose method above for a fully working setup.

## Running tests

```bash
cd vehicle-db-app
pip install -r requirements.txt
docker compose up -d db
DB_HOST=localhost pytest
```

## Stack

Python 3.12 · FastAPI · PostgreSQL 16 · Docker Compose · GitHub Actions (CI/CD)