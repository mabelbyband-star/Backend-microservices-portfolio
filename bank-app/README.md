# Bank App

A FastAPI service for managing bank accounts — registration, login, deposits, withdrawals, and transfers between accounts — backed by PostgreSQL, with hashed passwords and transaction history.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/accounts/register` | Create a new account (`name`, `last_name`, `email`, `password`, `opening_balance`) |
| POST | `/accounts/login` | Verify email and password |
| POST | `/accounts/{account_id}/deposit` | Add funds to an account |
| POST | `/accounts/{account_id}/withdraw` | Remove funds, fails if insufficient balance |
| POST | `/accounts/{account_id}/transfer` | Move funds from one account to another |
| GET | `/accounts/{account_id}/balance` | Current balance |
| GET | `/accounts/{account_id}/transactions` | Full transaction history for an account |

Interactive docs available at `/docs` once running.

## Security notes

- Passwords are hashed with `bcrypt` before being stored — never saved or compared as plain text.
- Transfers run inside a single database transaction: if any step fails (account not found, insufficient funds, a database error), all changes are rolled back, so a transfer can never leave money "stuck" between accounts.

## Run locally with Docker Compose (recommended)

This starts both the API and its PostgreSQL database, correctly networked together.

```bash
git clone https://github.com/mabelbyband-star/Backend-microservices-portfolio.git
cd Backend-microservices-portfolio/bank-app
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
docker pull erhb/bank-app
```

Note: the app expects a PostgreSQL database reachable at host `db` (or set the `DB_HOST` environment variable to point elsewhere). Running the image alone, without a database, will start the server but any endpoint touching the database will fail. Use the Docker Compose method above for a fully working setup.

## Running tests

```bash
cd bank-app
pip install -r requirements.txt
docker compose up -d db
DB_HOST=localhost pytest
```

## Stack

Python 3.12 · FastAPI · PostgreSQL 16 · bcrypt · Docker Compose · GitHub Actions (CI/CD)