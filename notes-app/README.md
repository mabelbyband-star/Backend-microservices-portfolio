# Notes API

A small FastAPI service for creating, listing, and deleting text notes, backed by PostgreSQL.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/notes` | Create a new note (`{"text": "..."}`) |
| GET | `/notes` | List all notes |
| DELETE | `/notes/{note_id}` | Delete a note by id |

Interactive docs available at `/docs` once running.

## Run locally with Docker Compose (recommended)

This starts both the API and its PostgreSQL database, correctly networked together.

```bash
git clone https://github.com/mabelbyband-star/Backend-microservices-portfolio.git
cd Backend-microservices-portfolio/notes-app
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
docker pull erhb/notes-app
```

Note: the app expects a PostgreSQL database reachable at host `db` (or set the `DB_HOST` environment variable to point elsewhere). Running the image alone, without a database, will start the server but any endpoint touching the database will fail. Use the Docker Compose method above for a fully working setup.

## Running tests

```bash
cd notes-app
pip install -r requirements.txt
docker compose up -d db
DB_HOST=localhost pytest
```

## Stack

Python 3.12 · FastAPI · PostgreSQL 16 · Docker Compose · GitHub Actions (CI/CD)
