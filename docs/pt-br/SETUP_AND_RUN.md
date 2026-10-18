# Guia de Instalação e Execução - Melitrack

Este guia fornece as instruções necessárias para configurar, construir e executar o ambiente de desenvolvimento ou produção do **Melitrack** utilizando Docker e Docker Compose.

---

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

- [**Docker Engine**](https://docs.docker.com/get-docker/) (v24.0+)
- [**Docker Compose**](https://docs.docker.com/compose/) (v2.20+)
- [**Python 3.12+**](https://www.python.org/) _(Opcional, apenas para desenvolvimento local sem containers)_
- [**Node.js 20+**](https://nodejs.org/) & `npm` _(Opcional, para desenvolvimento do frontend sem containers)_

---

## 1. Configuração de Variáveis de Ambiente

Crie os arquivos `.env` em cada subdiretório a partir dos modelos `.env.example` fornecidos no repositório:

### a) Raiz do Projeto (`.env`)

```bash
cp .env.example .env
```

Contém as credenciais do admin do Grafana:

```env
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin_seguro
```

### b) API Principal (`backend/api/.env`)

```bash
cp backend/api/.env.example backend/api/.env
```

Configure as senhas do PostgreSQL, MongoDB e segredos de JWT:

```env
POSTGRES_DB=melitrack_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_postgres
DB_HOST=db
DB_PORT=5432

API_PORT=8000
SECRET_KEY=seu_secret_key_jwt_super_seguro
ACCESS_TOKEN_EXPIRE_MINUTES=60

MONGO_DB=melitrack_photo
MONGO_URL=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority

ML_SERVICE_URL=http://ml:8000
ML_SERVICE_TOKEN=dev-ml-service-token
```

### c) Serviço de ML (`backend/ml/.env`)

```bash
cp backend/ml/.env.example backend/ml/.env
```

Configure a URL do Redis e token de comunicação interna:

```env
REDIS_URL=redis://redis:6379/0
ML_SERVICE_TOKEN=dev-ml-service-token
```

---

## 2. Criando a Rede Docker Compartilhada

Antes de subir os containers pela primeira vez, crie a rede externa `melitrack-network`:

```bash
docker network create melitrack-network
```

---

## 3. Executando a Aplicação via Docker Compose

Você pode subir a infraestrutura completa rodando os comandos abaixo na raiz do projeto:

### Passo A: Iniciar Banco de Dados & API Principal

```bash
cd backend/api
docker compose up -d --build
```

_Isso subirá o PostgreSQL (`melitrack_db`), MongoDB (`melitrack_photos`) e a API FastAPI (`melitrack-api`)._

### Passo B: Executar as Migrações do Banco de Dados (Alembic)

Com o PostgreSQL rodando, aplique as migrações para criar as tabelas relacioanais:

```bash
# Executa as migrações dentro do container da API
docker exec -it melitrack-api alembic upgrade head
```

### Passo C: Iniciar Serviço de ML & Celery Worker

```bash
cd ../ml
docker compose up -d --build
```

_Isso subirá o Redis (`melitrack_redis`), a ML API (`melitrack-ml`) e o Celery Worker (`melitrack-ml-worker`)._

### Passo D: Iniciar Pilha de Observabilidade (Grafana / Loki / Alloy)

```bash
cd ../../observability
docker compose up -d --build
```

### Passo E: Iniciar o Frontend (React)

Navegue até a pasta `frontend/`:

```bash
cd ../frontend
npm install
npm run dev
```

---

## 4. Endereços de Acesso às Aplicações

Após subir todos os serviços, os seguintes painéis e APIs estarão disponíveis:

| Aplicação / Serviço            | URL de Acesso                | Descrição / Credenciais                    |
| :----------------------------- | :--------------------------- | :----------------------------------------- |
| 💻 **Frontend Web**            | `http://localhost:5173`      | Interface React para os meliponicultores   |
| ⚡ **Swagger (API Principal)** | `http://localhost:8000/docs` | Documentação interativa FastAPI            |
| 🧠 **Swagger (ML API)**        | `http://localhost:8001/docs` | Documentação do microserviço de ML         |
| 📊 **Grafana Dashboard**       | `http://localhost:3000`      | Login: `admin` / Senha: definida no `.env` |
| 🪵 **Grafana Loki Logs**       | `http://localhost:3100`      | Endpoint de recepção de logs               |

---

## 🔍 5. Comandos Úteis de Monitoramento e Logs

Para acompanhar os logs de cada serviço em tempo real:

```bash
# Logs da API Principal
docker logs -f melitrack-api

# Logs do Worker de ML (Celery)
docker logs -f melitrack-ml-worker

# Logs do Coletor Grafana Alloy
docker logs -f melitrack-alloy
```

Para parar todos os containers:

```bash
docker compose -f backend/api/docker-compose.yml down
docker compose -f backend/ml/docker-compose.yml down
docker compose -f observability/docker-compose.yml down
```
