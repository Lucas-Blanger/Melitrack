# Melitrack - System Documentation (English)

Welcome to the official documentation for **Melitrack**, an intelligent and integrated platform for stingless hive management (*Meliponini*), field inspection logging, Computer Vision / AI analysis, harvest tracking, and real-time observability.

---

## Language Navigation

- 🇺🇸 **English Documentation** (Current)
- 🇧🇷 [**Documentação em Português**](../pt-br/README.md)

---

## Documentation Index

The documentation is organized into the following detailed guides:

| Document | Description |
| :--- | :--- |
| 🏗️ [**System Architecture**](ARCHITECTURE.md) | Overview of microservices, containerization, async task queues, and logging pipelines. |
| 🗄️ [**Database Model**](DATABASE.md) | Details of the hybrid storage strategy (PostgreSQL + MongoDB) and ER diagram. |
| 🔌 [**Services & APIs**](SERVICES_AND_API.md) | Specification of REST endpoints (FastAPI), JWT/OAuth authentication, rate limiting, and ML pipeline. |
| 🚀 [**Setup & Execution Guide**](SETUP_AND_RUN.md) | Step-by-step instructions to run the application via Docker Compose and configure environment variables. |

---

## Project Overview

**Melitrack** was developed to help stingless beekeepers manage their hives efficiently. The platform combines a modern, responsive frontend with a resilient microservices backend architecture enabling:

- **Hive Management**: Geolocated box registration, species catalog (*Jataí, Mandaçaia, Uruçu, Bugia, etc.*), box models (INPA, AF, etc.), and photo history.
- **Periodic Field Inspections**: Colony health tracking, queen presence, population estimates, honey reserves, and field notes.
- **AI Smart Analysis (ML)**: Asynchronous photo processing from inspections to identify species and evaluate colony health via computer vision.
- **Harvest & Product Control**: Tracking production of Honey, Propolis, Pollen, Geopropolis, and Wax with quantitative metrics.
- **Real-Time Observability**: Ecosystem log and metric collection and centralization via **Grafana, Loki, and Grafana Alloy**.
