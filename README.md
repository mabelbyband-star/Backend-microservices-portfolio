# Backend Microservices Portfolio

A collection of small backend projects demonstrating Python, FastAPI, Docker, PostgreSQL, and CI/CD with GitHub Actions. Built while learning backend development, moving from plain Python scripts to fully containerized, tested, and automatically deployed services.

## Why this repo

Each project follows the same progression: plain Python logic first (written and tested standalone), then wrapped in a FastAPI web service, then containerized with Docker, then connected to a real PostgreSQL database, and finally shipped through an automated CI/CD pipeline that tests, builds, and publishes a Docker image on every change.

## Projects

| Project | What it does | Tech stack |
|---|---|---|
| [`notes-app`](./notes-app) | A notes API — create, list, and delete text notes | Python, FastAPI, PostgreSQL, Docker |
| [`habit-tracker`](./habit-tracker) | A habit tracker that calculates the longest streak of consecutive completed days | Python, FastAPI, PostgreSQL, Docker |
| [`vehicle-db-app`](./vehicle-db-app) | An interactive vehicle customizer that saves each build to a database | Python, PostgreSQL, Docker |


`notes-app` and `habit-tracker` are the most complete examples — both are fully containerized, backed by PostgreSQL, and have their own independent CI/CD pipeline (tests → build → publish to Docker Hub) that runs automatically on every pull request and push to `main`.

## How to run a project

Each project folder has its own README with exact instructions, but the general pattern is:

```bash
git clone https://github.com/mabelbyband-star/Backend-microservices-portfolio.git
cd Backend-microservices-portfolio/notes-app   # or any other project folder
docker compose up -d
```

This starts the app and its database together, correctly networked. The API will be available at `http://localhost:8000`, with interactive docs at `/docs`.

## Stack

- **Python 3.12** for application logic
- **FastAPI** for the API layer
- **PostgreSQL 16** for persistence
- **Docker** + **Docker Compose** for containerization and local development
- **GitHub Actions** for CI/CD (automated testing, building, and publishing to Docker Hub)