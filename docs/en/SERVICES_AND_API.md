# Services & APIs - Melitrack

This document details the REST endpoints of the **Core API** (FastAPI) and the **ML API**, outlining security mechanisms, rate limits, authentication flows, and the computer vision processing pipeline.

---

## Authentication & Security

### 1. HttpOnly Cookie & JWT Header Authentication

The authentication system operates primarily through **Secure Cookies (`HttpOnly`)**:

- Upon login (`/auth/login` or `/auth/google/callback`), the API automatically sets a secure cookie named **`melitrack_session`** (`HttpOnly`, `SameSite=Lax`, 24-hour expiration).
- The backend extracts the token directly from this cookie on incoming requests.
- **HTTP Header Fallback**: If the client sends requests without cookies (e.g., API testing tools or external scripts), the backend also supports standard HTTP header authentication:
  ```http
  Authorization: Bearer <your_jwt_token>
  ```
- **Logout (`POST /auth/logout`)**: Clears the `melitrack_session` cookie from the browser.

### 2. Social Login (Google OAuth2)

- Integrated OAuth2 workflow for simplified user sign-in via Google.

### 3. Rate Limiter (Route Protection)

The system implements a custom IP-based request rate limiting middleware (`RateLimitMiddleware`) with category-specific rules:

| Route / Category                  | Request Limit  | Time Window        | Objective                              |
| :-------------------------------- | :------------- | :----------------- | :------------------------------------- |
| **General Default**               | 300 requests   | 60 seconds         | Prevent overall API abuse              |
| **Login (`/auth/login`)**         | 5 requests     | 60 seconds         | Prevent password brute-force attacks   |
| **Register (`/auth/register`)**   | 10 requests    | 3,600 seconds (1h) | Prevent automated account creation     |
| **Password Reset**                | 3 requests     | 900 seconds (15m)  | Prevent email flooding                 |
| **Google OAuth (`/auth/google`)** | 20 requests    | 60 seconds         | Limit OAuth flow abuse                 |

---

## Core API Endpoints (Port 8000)

### Auth & User Management (`/auth`)

| Method | Route                   | Authenticated? | Description                                       |
| :----- | :---------------------- | :------------- | :------------------------------------------------ |
| `POST` | `/auth/register`        | No             | Register new stingless beekeeper account          |
| `POST` | `/auth/login`           | No             | Local authentication & JWT cookie issuance        |
| `GET`  | `/auth/me`              | **Yes**        | Return authenticated user profile details         |
| `PUT`  | `/auth/me`              | **Yes**        | Update profile details and meliponary preferences |
| `POST` | `/auth/forgot-password` | No             | Request password reset code via email             |
| `POST` | `/auth/reset-password`  | No             | Reset password using confirmation code            |
| `GET`  | `/auth/google`          | No             | Initiate Google OAuth2 authentication flow        |
| `GET`  | `/auth/google/callback` | No             | Google OAuth2 callback endpoint                   |

---

### Hive Management (`/hives`)

| Method   | Route                                | Authenticated? | Description                                                        |
| :------- | :----------------------------------- | :------------- | :----------------------------------------------------------------- |
| `GET`    | `/hives`                             | **Yes**        | List all hives belonging to user                                   |
| `POST`   | `/hives`                             | **Yes**        | Register a new hive (name, species, model, location)               |
| `GET`    | `/hives/{hive_id}`                   | **Yes**        | Get details for a specific hive                                    |
| `PUT`    | `/hives/{hive_id}`                   | **Yes**        | Update hive details                                                |
| `DELETE` | `/hives/{hive_id}`                   | **Yes**        | Remove a hive and cascade-delete inspections/photos                |
| `GET`    | `/hives/{hive_id}/photos`            | **Yes**        | List hive photos stored in MongoDB                                 |
| `POST`   | `/hives/{hive_id}/photos`            | **Yes**        | Upload a hive photo (max 10MB)                                     |
| `DELETE` | `/hives/{hive_id}/photos/{photo_id}` | **Yes**        | Remove a specific photo from MongoDB                               |

---

### Inspections & Photo Analysis (`/hives/{hive_id}/inspections`)

| Method  | Route                                             | Authenticated? | Description                                             |
| :------ | :------------------------------------------------ | :------------- | :------------------------------------------------------ |
| `GET`   | `/hives/{hive_id}/inspections`                    | **Yes**        | List all inspections for a hive                         |
| `POST`  | `/hives/{hive_id}/inspections`                    | **Yes**        | Register a new field inspection                         |
| `GET`   | `/hives/{hive_id}/inspections/{id}`               | **Yes**        | Inspection details, including AI prediction             |
| `POST`  | `/hives/{hive_id}/inspections/{id}/photos`        | **Yes**        | Upload inspection photo & trigger ML analysis pipeline  |
| `PATCH` | `/hives/{hive_id}/inspections/{id}/ml-correction` | **Yes**        | Allow user to manually correct AI prediction results    |

---

### Harvests & Products (`/harvests` & `/products`)

| Method | Route        | Authenticated? | Description                                                      |
| :----- | :----------- | :------------- | :--------------------------------------------------------------- |
| `GET`  | `/products` | **Yes**        | List available product catalog (Honey, Propolis, Pollen, etc.)   |
| `POST` | `/products` | **Yes**        | Add a new product category to catalog                            |
| `GET`  | `/harvests` | **Yes**        | List harvest history for user                                    |
| `POST` | `/harvests` | **Yes**        | Record product extraction from a hive                            |

---

### Health Service (`/health`)

| Method | Route      | Description                                                    |
| :----- | :--------- | :------------------------------------------------------------- |
| `GET`  | `/health` | Verify API health status and PostgreSQL / MongoDB connections  |

---

## ML Service Endpoints (Port 8001)

The ML microservice accepts incoming connections secured by an internal secret header token:
`X-ML-Service-Token: <ML_SERVICE_TOKEN>`

| Method | Route       | Description                                                                                          |
| :----- | :---------- | :--------------------------------------------------------------------------------------------------- |
| `POST` | `/analyze` | Receives `inspection_id` and Base64 image payload, enqueuing Celery/Redis task. Returns `202 Accepted`. |
| `GET`  | `/species` | Returns list of supported stingless bee species for trained model.                                   |
| `GET`  | `/health`  | Health status of ML service and Redis connectivity.                                                  |

---

## Error Handling & Response Standards

In case of errors on the Core API, responses conform to RFC 7807 using semantic HTTP status codes:

- **`400 Bad Request`**: Invalid input data, empty image, or file exceeding 10MB limit.
- **`401 Unauthorized`**: Missing or expired JWT token / invalid ML service token.
- **`404 Not Found`**: Hive, inspection, or photo record not found.
- **`429 Too Many Requests`**: Rate limit exceeded.
- **`500 Internal Server Error`**: Unhandled server error.

Example error response body:

```json
{
  "detail": "Imagem maior que 10MB"
}
```
