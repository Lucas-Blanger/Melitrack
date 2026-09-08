# Database Model - Melitrack

**Melitrack** adopts a **polyglot (hybrid)** storage strategy, combining the relational integrity of **PostgreSQL** for core business logic with the high-performance NoSQL capabilities of **MongoDB** for binary image and photo media storage.

---

## Database Diagram

The official entity-relationship (ER) diagram for the project is available at:
[**View Database Diagram**](../melitrack_db%20.png)

![Melitrack Database Diagram](../melitrack_db%20.png)

---

## 1. Relational Database (PostgreSQL)

**PostgreSQL 16** is managed via the **SQLAlchemy 2.0** ORM, with schema versioning controlled through **Alembic**.

### Enum Types

- **`HiveType`**:
  - `inpa`: Standard INPA box (Nest, Super, Honey Super modules).
  - `af`: Standard AF box (AF-1 / AF-2).
  - `troncofixo`: Natural log or fixed trunk rational hive.
  - `outro`: Other artisanal models or custom hives.

- **`ColonyHealth`**:
  - `excelente`: Strong colony, abundant food reserves, excellent brood posture.
  - `boa`: Healthy colony progressing normally.
  - `alerta`: Signs of vulnerability, phorid fly attacks, or food shortage.
  - `critica`: Imminent risk of colony collapse or hive abandonment.

- **`AnalysisStatus`**:
  - `pending`: Computer vision analysis queued or awaiting processing.
  - `processing`: Inference actively being run by the Celery Worker.
  - `completed`: AI prediction completed successfully.
  - `failed`: Image processing failure or invalid format.
  - `corrected`: AI result manually corrected by the beekeeper.

---

### PostgreSQL Tables

#### 1. `users` (System Users)

Stores beekeeper accounts, access credentials, and meliponary preferences.

| Column                      | Type          | Constraints                  | Description                                 |
| :-------------------------- | :------------ | :--------------------------- | :------------------------------------------ |
| `id`                        | `UUID`        | PK, Default: `uuid4()`       | Unique user identifier                      |
| `name`                      | `VARCHAR`     | NOT NULL                     | Full name                                   |
| `email`                     | `VARCHAR`     | NOT NULL, UNIQUE, INDEX      | Login email address                         |
| `hashed_password`           | `VARCHAR`     | NOT NULL                     | Encrypted password (Bcrypt)                 |
| `is_active`                 | `BOOLEAN`     | Default: `true`              | Account status                              |
| `auth_provider`             | `VARCHAR`     | NOT NULL, Default: `'local'` | Auth provider (`local`, `google`)           |
| `google_id`                 | `VARCHAR`     | UNIQUE, NULLABLE             | Google profile ID                           |
| `picture`                   | `VARCHAR`     | NULLABLE                     | Profile picture URL                         |
| `reset_code`                | `VARCHAR`     | NULLABLE                     | Password recovery verification code         |
| `reset_code_expires`        | `TIMESTAMPTZ` | NULLABLE                     | Password recovery code expiration           |
| `meliponary_name`           | `VARCHAR`     | Default: `'Meu Meliponário'` | Custom meliponary name                      |
| `meliponary_location`       | `VARCHAR`     | NULLABLE                     | General location of the meliponary          |
| `inspection_frequency_days` | `INTEGER`     | Default: `14`                | Suggested inspection frequency (days)       |
| `notify_health_alerts`      | `BOOLEAN`     | Default: `true`              | Notify health alerts                        |
| `notify_email`              | `BOOLEAN`     | Default: `true`              | Receive email notifications                 |
| `created_at` / `updated_at` | `TIMESTAMPTZ` | Default: `now()`             | Audit timestamps                            |

---

#### 2. `hives` (Stingless Bee Hives)

Stores rational hives registered by the user.

| Column                      | Type             | Constraints                       | Description                                      |
| :-------------------------- | :--------------- | :-------------------------------- | :----------------------------------------------- |
| `id`                        | `UUID`           | PK, Default: `uuid4()`            | Unique hive ID                                   |
| `owner_id`                  | `UUID`           | FK -> `users.id`, NOT NULL, INDEX | Hive owner                                       |
| `name`                      | `VARCHAR(150)`   | NOT NULL                          | Hive name or identifier (e.g., _Jataí-01_)       |
| `type`                      | `ENUM(HiveType)` | NOT NULL                          | Box model (`inpa`, `af`, etc.)                   |
| `species`                   | `VARCHAR(100)`   | NOT NULL                          | Species name (_Tetragonisca angustula_, etc.)    |
| `latitude`                  | `FLOAT`          | NULLABLE                          | GPS Coordinate (Latitude)                        |
| `longitude`                 | `FLOAT`          | NULLABLE                          | GPS Coordinate (Longitude)                       |
| `location_description`      | `VARCHAR(255)`   | NULLABLE                          | Location description (e.g., _Near the orchard_)  |
| `notes`                     | `TEXT`           | NULLABLE                          | Additional notes                                 |
| `created_at` / `updated_at` | `TIMESTAMPTZ`    | Default: `now()`                  | Timestamps                                       |

---

#### 3. `inspections` (Field Inspection Logs)

Records of periodic hive checks.

| Column                | Type                 | Constraints                                 | Description                                     |
| :-------------------- | :------------------- | :------------------------------------------ | :---------------------------------------------- |
| `id`                  | `UUID`               | PK, Default: `uuid4()`                      | Unique inspection ID                            |
| `hive_id`             | `UUID`               | FK -> `hives.id` (ON DELETE CASCADE), INDEX | Hive inspected                                  |
| `owner_id`            | `UUID`               | FK -> `users.id`, INDEX                     | Owner                                           |
| `health`              | `ENUM(ColonyHealth)` | NOT NULL                                    | Colony health evaluation                        |
| `queen_seen`          | `BOOLEAN`            | NULLABLE                                    | Queen sighting boolean                          |
| `honey_level`         | `INTEGER`            | NULLABLE                                    | Honey level estimate (scale 1 to 5)             |
| `population_estimate` | `VARCHAR(50)`        | NULLABLE                                    | Population estimate (_low_, _medium_, _high_)   |
| `notes`               | `TEXT`               | NULLABLE                                    | Field observations during inspection            |
| `inspected_at`        | `TIMESTAMPTZ`        | Default: `now()`                            | Inspection date and time                        |

---

#### 4. `ml_predictions` (Artificial Intelligence Inference Results)

Computer vision predictions linked to an inspection.

| Column             | Type                   | Constraints                              | Description                                      |
| :----------------- | :--------------------- | :--------------------------------------- | :----------------------------------------------- |
| `id`               | `UUID`                 | PK, Default: `uuid4()`                   | Unique ML record ID                              |
| `inspection_id`    | `UUID`                 | FK -> `inspections.id`, UNIQUE, NOT NULL | Linked inspection (1-to-1 relationship)          |
| `status`           | `ENUM(AnalysisStatus)` | Default: `'pending'`                     | AI processing status                             |
| `model_name`       | `VARCHAR(100)`         | NULLABLE                                 | Model name/version used                          |
| `result`           | `JSONB`                | NULLABLE                                 | Inference payload (species, score, health)       |
| `confidence`       | `FLOAT`                | NULLABLE                                 | Model confidence score (0.0 to 1.0)              |
| `error_message`    | `TEXT`                 | NULLABLE                                 | Error message if Celery worker failed            |
| `corrected_result` | `JSONB`                | NULLABLE                                 | Manually corrected result payload by beekeeper   |
| `correction_notes` | `TEXT`                 | NULLABLE                                 | Correction rationale/notes                       |
| `corrected_at`     | `TIMESTAMPTZ`          | NULLABLE                                 | Manual correction timestamp                      |
| `processed_at`     | `TIMESTAMPTZ`          | NULLABLE                                 | AI processing completion timestamp               |

---

#### 5. `products` (Stingless Beekeeping Products)

Catalog of bee products.

| Column        | Type           | Constraints       | Description                                            |
| :------------ | :------------- | :---------------- | :----------------------------------------------------- |
| `id`          | `SERIAL`       | PK, Autoincrement | Product ID                                             |
| `name`        | `VARCHAR(100)` | UNIQUE, NOT NULL  | Product name (_Honey_, _Propolis_, _Wax_, _Pollen_)    |
| `unit`        | `VARCHAR(20)`  | NOT NULL          | Standard measurement unit (`ml`, `g`, `kg`)            |
| `description` | `TEXT`         | NULLABLE          | Product description                                    |
| `is_active`   | `BOOLEAN`      | Default: `true`   | Catalog active status                                  |

---

#### 6. `harvests` (Harvest Records)

Logs of harvests extracted from hives.

| Column          | Type          | Constraints             | Description                                     |
| :-------------- | :------------ | :---------------------- | :---------------------------------------------- |
| `id`            | `UUID`        | PK, Default: `uuid4()`  | Unique harvest ID                               |
| `hive_id`       | `UUID`        | FK -> `hives.id`, INDEX | Source hive                                     |
| `owner_id`      | `UUID`        | FK -> `users.id`        | Owner                                           |
| `product_id`    | `INTEGER`     | FK -> `products.id`     | Harvested product                               |
| `quantity`      | `FLOAT`       | NOT NULL                | Harvested quantity                              |
| `unit`          | `VARCHAR(20)` | NOT NULL                | Measurement unit                                |
| `quality_notes` | `TEXT`        | NULLABLE                | Quality notes (color, flavor, moisture content) |
| `harvested_at`  | `TIMESTAMPTZ` | Default: `now()`        | Extraction date                                 |

---

## 2. NoSQL Database (MongoDB)

**MongoDB 8** is accessed completely asynchronously using the **Motor** library. It is responsible for storing user-submitted images as binary data (`bytes`), preventing bloating of the relational database.

### Collection: `hive_photos`

Stores general photos of the hive structure or meliponary.

```json
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d0"),
  "owner_id": "user-uuid-string",
  "hive_id": "hive-uuid-string",
  "filename": "hive_box.jpg",
  "content_type": "image/jpeg",
  "size": 2450800,
  "data": Binary(Buffer),
  "uploaded_at": ISODate("2026-09-04T12:00:00Z")
}
```

### Collection: `inspection_photos`

Stores internal photos taken during an inspection and sent for ML computer vision processing.

```json
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d1"),
  "owner_id": "user-uuid-string",
  "hive_id": "hive-uuid-string",
  "inspection_id": "inspection-uuid-string",
  "filename": "brood_comb.jpg",
  "content_type": "image/jpeg",
  "size": 1820400,
  "data": Binary(Buffer),
  "uploaded_at": ISODate("2026-09-04T12:05:00Z"),
  "ml_status": "pending"
}
```

> **Design Note**: In REST API responses (`PhotoResponse`), the binary `data` field stores the file and is dynamically transformed into a Data URI string (`data:image/jpeg;base64,...`) for direct rendering inside React `<img>` tags without requiring separate media server infrastructure.
