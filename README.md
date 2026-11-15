# WorkFlow – Team Task Management API

A team task management backend API built with **FastAPI** and **SQLAlchemy**. The project provides API endpoints for managing users, projects, tasks, and comments, with JWT-based authentication, Redis caching, automated tests, and Docker-based deployment.

## Tech Stack

- **Python 3.13**
- **FastAPI** – REST API development
- **SQLAlchemy** – ORM and database interaction
- **SQLite** – Database
- **JWT** – Authentication
- **Passlib + bcrypt** – Password hashing
- **Redis** – Data caching
- **Alembic** – Database migrations
- **Pytest** – Automated testing
- **Locust** – Load testing
- **Docker & Docker Compose** – Containerization
- **GitHub Actions** – Continuous Integration (CI)

## Features

- REST API endpoints for users, projects, tasks, and comments
- JWT-based authentication
- Secure password hashing using bcrypt
- Token expiration and validation
- Admin role verification
- Redis caching for project data
- Database schema migrations with Alembic
- Automated tests with Pytest
- API load testing with Locust

## Project Structure

```text
WorkFlow/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── permissions.py
│   │   ├── redis.py
│   │   └── security.py
│   │
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── main.py
│
├── locust/
├── tests/
│
├── Dockerfile
├── compose.yaml
├── alembic.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd WorkFlow
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
SQLALCHEMY_DATABASE_URL=sqlite:///./workflow.db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use a secure secret key for your own environment. Never commit real credentials or secret keys to GitHub.

### 3. Install dependencies

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## Docker Compose

The project includes Docker Compose configuration for running the application with Redis and Locust.

Build and start the services:

```bash
docker compose up --build
```

The application runs database migrations before starting the FastAPI server.

Available services:

| Service | Address |
|---|---|
| FastAPI | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Redis | localhost:6380 |
| Locust | http://localhost:8089 |

The Docker Compose configuration uses a persistent Docker volume for SQLite database storage.

To stop the services:

```bash
docker compose down
```

## Testing

Run automated tests using Pytest:

```bash
python -m pytest -v
```

## Performance Testing

Load testing was performed using Locust.

**Latest recorded test configuration:**

- Duration: 5 minutes
- Concurrent users: 30
- Spawn rate: 3 users/second
- Tested endpoints:
  - `POST /users/login/`
  - `GET /projects/`

**Results:**

| Metric | Result |
|---|---:|
| Total requests | 4,455 |
| Failed requests | 0 |
| Failure rate | 0% |
| Average response time | 22.04 ms |
| Median response time | 14 ms |
| 95th percentile | 35 ms |
| 99th percentile | 83 ms |

These results represent a local load test and should not be interpreted as production performance guarantees.

## Continuous Integration

GitHub Actions is configured to run automated tests when code is pushed to or a pull request is opened against the `main` branch.

The workflow:
1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Runs the Pytest test suite.

---

**WorkFlow** – A backend project focused on API development, authentication, caching, database management, automated testing, and containerization.