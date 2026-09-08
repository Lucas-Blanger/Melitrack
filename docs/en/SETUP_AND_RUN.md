# Setup & Execution Guide - Melitrack

This guide provides instructions to configure, build, and run **Melitrack** in development or production environments using Docker and Docker Compose.

---

## Prerequisites

Before starting, ensure the following prerequisites are installed on your system:

- [**Docker Engine**](https://docs.docker.com/get-docker/) (v24.0+)
- [**Docker Compose**](https://docs.docker.com/compose/) (v2.20+)
- [**Python 3.12+**](https://www.python.org/) _(Optional, only for local non-containerized backend development)_
- [**Node.js 20+**](https://nodejs.org/) & `npm` _(Optional, for non-containerized frontend development)_

---

## 1. Environment Variable Configuration

Create `.env` files in each subdirectory based on the provided `.env.example` templates in the repository:

### a) Project Root (`.env`)

```bash
cp .env.example .env
```

Contains Grafana administrator credentials:

```env
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=secure_admin_password
```

### b) Core API (`backend/api/.env`)

```bash
cp backend/api/.env.example backend/api/.env
```

Configure PostgreSQL, MongoDB passwords, and JWT secret keys:

```env
POSTGRES_DB=melitrack_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
DB_HOST=db
DB_PORT=5432

API_PORT=8000
SECRET_KEY=your_super_secret_jwt_key
ACCESS_TOKEN_EXPIRE_MINUTES=60

MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=your_mongo_password
MONGO_DB=melitrack_photo
MONGO_URL=mongodb://admin:your_mongo_password@mongo:27017/?authSource=admin

ML_SERVICE_URL=http://ml:8000
ML_SERVICE_TOKEN=dev-ml-service-token
```

### c) ML Service (`backend/ml/.env`)

```bash
cp backend/ml/.env.example backend/ml/.env
```

Configure Redis URL and internal service token:

```env
REDIS_URL=redis://redis:6379/0
ML_SERVICE_TOKEN=dev-ml-service-token
```

---

## 2. Creating the Shared Docker Network

Before spinning up containers for the first time, create the external `melitrack-network` bridge:

```bash
docker network create melitrack-network
```

---

## 3. Running the Application via Docker Compose

Run the infrastructure stack using the following steps from the project root:

### Step A: Start Databases & Core API

```bash
cd backend/api
docker compose up -d --build
```

_This starts PostgreSQL (`melitrack_db`), MongoDB (`melitrack_photos`), and the Core FastAPI app (`melitrack-api`)._

### Step B: Apply Database Migrations (Alembic)

With PostgreSQL running, apply migrations to create relational tables:

```bash
# Execute migrations inside the API container
docker exec -it melitrack-api alembic upgrade head
```

### Step C: Start ML Service & Celery Worker

```bash
cd ../ml
docker compose up -d --build
```

_This starts Redis (`melitrack_redis`), ML API (`melitrack-ml`), and the Celery Worker (`melitrack-ml-worker`)._

### Step D: Start Observability Stack (Grafana / Loki / Alloy)

```bash
cd ../../observability
docker compose up -d --build
```

### Step E: Start Frontend (React)

Navigate to `frontend/`:

```bash
cd ../frontend
npm install
npm run dev
```

---

## 4. Application Access URLs

Once all services are running, access the following endpoints:

| Application / Service          | Access URL                   | Description / Credentials                  |
| :----------------------------- | :--------------------------- | :----------------------------------------- |
| 💻 **Frontend Web**            | `http://localhost:5173`      | React interface for beekeepers             |
| ⚡ **Swagger (Core API)**      | `http://localhost:8000/docs` | Interactive FastAPI documentation          |
| 🧠 **Swagger (ML API)**        | `http://localhost:8001/docs` | ML microservice OpenAPI docs               |
| 📊 **Grafana Dashboard**       | `http://localhost:3000`      | Login: `admin` / Password: set in `.env`   |
| 🪵 **Grafana Loki Logs**       | `http://localhost:3100`      | Log aggregation push endpoint              |

---

## 🔍 5. Monitoring & Useful Logging Commands

To tail logs for each service in real time:

```bash
# Core API logs
docker logs -f melitrack-api

# ML Celery Worker logs
docker logs -f melitrack-ml-worker

# Grafana Alloy Collector logs
docker logs -f melitrack-alloy
```

To shut down all containers:

```bash
docker compose -f backend/api/docker-compose.yml down
docker compose -f backend/ml/docker-compose.yml down
docker compose -f observability/docker-compose.yml down
```
