# System Architecture - Melitrack

**Melitrack** is built under a highly modular, microservices-oriented architecture based on Docker containers and decoupled into three main pillars: **Web Application (SPA/API)**, **Artificial Intelligence / ML Service**, and **Observability Stack**.

---

## Architecture Overview

The diagram below illustrates Melitrack's complete ecosystem, highlighting components, databases, inter-service communication, and log flow:

```mermaid
flowchart TB
    subgraph Client["Client / Browser"]
        UI["Frontend (React 19 + Vite)"]
    end

    subgraph API_Stack["Core API (FastAPI)"]
        API["FastAPI Web Server<br/>(Port 8000)"]
        AUTH["Auth Module<br/>(JWT & Google OAuth)"]
        HIVES_APP["Hives & Inspections Module"]
        LIMITER["Rate Limit Middleware"]
    end

    subgraph ML_Stack["Artificial Intelligence Service"]
        ML_API["ML FastAPI Endpoint<br/>(Port 8001)"]
        CELERY["Celery Worker<br/>(Thread Pool)"]
        REDIS[("Redis 7 Broker<br/>(Port 6379)")]
        KERAS["Computer Vision Models<br/>(TensorFlow / Keras)"]
    end

    subgraph Storage["Data & Media Layer"]
        PG[("PostgreSQL 16<br/>(Structured Data)")]
        MONGO[("MongoDB 8<br/>(Photo Storage)")]
    end

    subgraph Observability["Observability Stack"]
        ALLOY["Grafana Alloy Agent<br/>(Tailing Logs)"]
        LOKI["Grafana Loki<br/>(Log Aggregator - Port 3100)"]
        GRAFANA["Grafana Dashboard<br/>(UI - Port 3000)"]
    end

    %% Frontend Connections
    UI -->|"HTTPS / REST API"| API

    %% API Connections
    API --> LIMITER
    LIMITER --> AUTH
    LIMITER --> HIVES_APP
    HIVES_APP -->|"SQLAlchemy"| PG
    HIVES_APP -->|"Motor Async"| MONGO
    HIVES_APP -->|"POST /analyze (Internal Token)"| ML_API

    %% ML Connections
    ML_API -->|"Enqueues Tasks"| REDIS
    CELERY -->|"Consumes 'ml' Queue"| REDIS
    CELERY --> KERAS
    CELERY -->|"Updates status and result"| PG

    %% Observability Connections
    API -.->|"Writes api.log"| LOG_FILES["/var/log/melitrack/*.log"]
    ML_API -.->|"Writes ml.log"| LOG_FILES
    CELERY -.->|"Writes ml-worker.log"| LOG_FILES
    ALLOY -->|"Reads log files"| LOG_FILES
    ALLOY -->|"Sends logs"| LOKI
    GRAFANA -->|"Queries logs"| LOKI
```

---

## System Components

### 1. Frontend (`frontend/`)

- **Technologies**: React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons, React Router DOM.
- **Role**: User interface for stingless beekeepers. Allows registering and viewing hives on a map, uploading photos, recording inspections, tracking AI analysis results, and monitoring honey and byproduct production.

### 2. Core Backend API (`backend/api/`)

- **Technologies**: FastAPI, Python 3.12, SQLAlchemy ORM, Alembic, Motor (MongoDB Async), PyJWT, Passlib.
- **Role**: Serves as the API gateway and orchestrator of main business rules.
- **Highlights**:
  - **Hybrid Authentication**: Local password login (Bcrypt) + Social login via Google OAuth.
  - **Rate Limiter Middleware**: Protection against abuse and brute-force attacks (default rate limit and custom limits for auth/password reset).
  - **Polyglot Persistence**: Uses PostgreSQL for strict relational data and MongoDB for high-volume binary photo data.

### 3. Backend ML Service (`backend/ml/`)

- **Technologies**: FastAPI, Celery 5, Redis 7, TensorFlow/Keras, iNaturalist Client.
- **Role**: Service dedicated to compute-heavy artificial intelligence and computer vision tasks.
- **Asynchronous Architecture**:
  1. Core API sends a `POST /analyze` request to the ML API containing the inspection ID and Base64-encoded image, protected by an internal token (`X-ML-Service-Token`).
  2. ML API creates a task in **Redis** and immediately responds with `202 Accepted` and the `task_id`.
  3. The **Celery Worker** consumes the task from the `ml` queue, runs inference on the Keras model (`species_model.keras`), and saves the final result directly to the `ml_predictions` table in PostgreSQL.

### 4. Observability Stack (`observability/`)

- **Components**:
  - **Grafana Alloy**: Lightweight log collection agent monitoring the shared log directory `/var/log/melitrack/` (`api.log`, `ml.log`, `ml-worker.log`).
  - **Grafana Loki**: Log aggregation engine storing indexed logs by labels.
  - **Grafana**: Web dashboard for graphical log queries and system alerts.

---

## Network & Docker Compose Topology

All services communicate securely across a shared Docker bridge network named `melitrack-network`:

| Container Service | Container Name        | Internal Port | Host Port Exposed       | Role                        |
| :---------------- | :-------------------- | :------------ | :---------------------- | :-------------------------- |
| `api`             | `melitrack-api`       | 8000          | `${API_PORT}` (8000)    | Core API Server             |
| `db`              | `melitrack_db`        | 5432          | `${DB_PORT}` (5432)     | PostgreSQL Relational DB    |
| `mongo`           | `melitrack_photos`    | 27017         | `${MONGO_PORT}` (27017) | MongoDB NoSQL Database      |
| `ml`              | `melitrack-ml`        | 8000          | `${ML_PORT}` (8001)     | ML API Server               |
| `ml-worker`       | `melitrack-ml-worker` | -             | -                       | Celery Worker for ML        |
| `redis`           | `melitrack_redis`     | 6379          | `${REDIS_PORT}` (6379)  | Queue & Cache               |
| `loki`            | `melitrack-loki`      | 3100          | 3100                    | Log Aggregator              |
| `alloy`           | `melitrack-alloy`     | 12345         | 12345                   | Log Collector               |
| `grafana`         | `melitrack-grafana`   | 3000          | 3000                    | Monitoring UI               |

---

## Photo & AI Processing Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Beekeeper
    participant Web as Frontend (React)
    participant API as Core FastAPI
    participant Mongo as MongoDB
    participant PG as PostgreSQL
    participant ML as FastAPI ML
    participant Redis as Redis Queue
    participant Worker as Celery Worker

    User->>Web: Uploads Inspection Photo
    Web->>API: POST /hives/{hive_id}/inspections/{id}/photos
    API->>Mongo: Saves photo binary in 'inspection_photos'
    API->>PG: Creates record in 'inspection_photos' and 'ml_predictions' (Status: PENDING)
    API->>ML: POST /analyze (sends image payload & inspection_id)
    ML->>Redis: Enqueues 'analyze_hive_photo' task in 'ml' queue
    ML-->>API: 202 Accepted (task_id)
    API-->>Web: Returns confirmation and PhotoResponse

    Note over Worker,Redis: Asynchronous Processing
    Worker->>Redis: Pops task from queue
    Worker->>Worker: Executes Keras Model Inference
    Worker->>PG: Updates 'ml_predictions' (Status: COMPLETED / FAILED, result, confidence)

    Web->>API: GET /hives/{hive_id}/inspections/{id}
    API->>PG: Queries inspection + ml_predictions
    API-->>Web: Returns inspection data updated with AI prediction
```
