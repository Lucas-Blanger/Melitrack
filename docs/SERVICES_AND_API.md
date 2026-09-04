# Serviços & APIs - Melitrack

Este documento descreve os endpoints REST da **API Principal** (FastAPI) e da **ML API**, detalhando mecanismos de segurança, limites de acesso, autenticação e pipeline de análise por visão computacional.

---

## Autenticação & Segurança

### 1. Autenticação por Cookie HttpOnly & Header JWT

O sistema de autenticação opera principalmente através de **Cookies Seguros (`HttpOnly`)**:

- No login (`/auth/login` ou `/auth/google/callback`), a API define automaticamente um cookie seguro chamado **`melitrack_session`** (`HttpOnly`, `SameSite=Lax`, expiração de 24h).
- O backend extrai o token diretamente deste Cookie nas requisições.
- **Fallback HTTP Header**: Caso o cliente envie requisições sem cookies (ex: ferramentas de teste ou scripts externos), o backend também suporta autenticação pelo cabeçalho HTTP tradicional:
  ```http
  Authorization: Bearer <seu_jwt_token>
  ```
- **Logout (`POST /auth/logout`)**: Remove o cookie `melitrack_session` do navegador.

### 2. Login Social (Google OAuth2)

- Fluxo de autenticação OAuth2 integrado para login simplificado de usuários via Google.

### 3. Rate Limiter (Proteção de Rotas)

O sistema implementa um middleware customizado de limitação de requisições por IP (`RateLimitMiddleware`) com regras diferenciadas:

| Rota / Categoria                  | Limite de Requisições | Janela de Tempo     | Objetivo                              |
| :-------------------------------- | :-------------------- | :------------------ | :------------------------------------ |
| **Padrão Geral**                  | 300 requisições       | 60 segundos         | Prevenir abuso geral da API           |
| **Login (`/auth/login`)**         | 5 requisições         | 60 segundos         | Prevenir força bruta em senhas        |
| **Registro (`/auth/register`)**   | 10 requisições        | 3.600 segundos (1h) | Evitar criação automatizada de contas |
| **Recuperação de Senha**          | 3 requisições         | 900 segundos (15m)  | Evitar flooding de e-mails de reset   |
| **Google OAuth (`/auth/google`)** | 20 requisições        | 60 segundos         | Limitar abuso no fluxo de OAuth       |

---

## Endpoints da API Principal (Porta 8000)

### Autenticação & Usuário (`/auth`)

| Método | Rota                    | Autenticado? | Descrição                                              |
| :----- | :---------------------- | :----------- | :----------------------------------------------------- |
| `POST` | `/auth/register`        | Não          | Cadastro de novo meliponicultor                        |
| `POST` | `/auth/login`           | Não          | Autenticação local e emissão de JWT                    |
| `GET`  | `/auth/me`              | **Sim**      | Retorna os dados do perfil do usuário autenticado      |
| `PUT`  | `/auth/me`              | **Sim**      | Atualiza dados do perfil e preferências do meliponário |
| `POST` | `/auth/forgot-password` | Não          | Solicita código de recuperação de senha por e-mail     |
| `POST` | `/auth/reset-password`  | Não          | Redefine a senha utilizando o código enviado           |
| `GET`  | `/auth/google`          | Não          | Inicia o fluxo de autenticação com o Google            |
| `GET`  | `/auth/google/callback` | Não          | Callback do Google OAuth2                              |

---

### Gestão de Colmeias (`/hives`)

| Método   | Rota                                 | Autenticado? | Descrição                                                         |
| :------- | :----------------------------------- | :----------- | :---------------------------------------------------------------- |
| `GET`    | `/hives`                             | **Sim**      | Lista todas as colmeias do usuário                                |
| `POST`   | `/hives`                             | **Sim**      | Cadastra uma nova colmeia (nome, espécie, modelo, geolocalização) |
| `GET`    | `/hives/{hive_id}`                   | **Sim**      | Obtém detalhes de uma colmeia específica                          |
| `PUT`    | `/hives/{hive_id}`                   | **Sim**      | Atualiza dados da colmeia                                         |
| `DELETE` | `/hives/{hive_id}`                   | **Sim**      | Remove uma colmeia e suas inspeções/fotos em cascata              |
| `GET`    | `/hives/{hive_id}/photos`            | **Sim**      | Lista as fotos da colmeia armazenadas no MongoDB                  |
| `POST`   | `/hives/{hive_id}/photos`            | **Sim**      | Envia uma foto da colmeia (máx 10MB)                              |
| `DELETE` | `/hives/{hive_id}/photos/{photo_id}` | **Sim**      | Remove uma foto específica no MongoDB                             |

---

### Inspeções & Análise Fotográfica (`/hives/{hive_id}/inspections`)

| Método  | Rota                                              | Autenticado? | Descrição                                              |
| :------ | :------------------------------------------------ | :----------- | :----------------------------------------------------- |
| `GET`   | `/hives/{hive_id}/inspections`                    | **Sim**      | Lista todas as inspeções da colmeia                    |
| `POST`  | `/hives/{hive_id}/inspections`                    | **Sim**      | Registra uma nova inspeção de campo                    |
| `GET`   | `/hives/{hive_id}/inspections/{id}`               | **Sim**      | Detalhes da inspeção, incluindo predição de IA         |
| `POST`  | `/hives/{hive_id}/inspections/{id}/photos`        | **Sim**      | Envia foto da inspeção e dispara a análise no ML       |
| `PATCH` | `/hives/{hive_id}/inspections/{id}/ml-correction` | **Sim**      | Permite ao usuário corrigir o resultado gerado pela IA |

---

### Colheitas & Produtos (`/harvests` & `/products`)

| Método | Rota        | Autenticado? | Descrição                                                      |
| :----- | :---------- | :----------- | :------------------------------------------------------------- |
| `GET`  | `/products` | **Sim**      | Lista o catálogo de produtos disponíveis (Mel, Própolis, etc.) |
| `POST` | `/products` | **Sim**      | Adiciona um novo produto ao catálogo                           |
| `GET`  | `/harvests` | **Sim**      | Lista o histórico de colheitas do usuário                      |
| `POST` | `/harvests` | **Sim**      | Registra a extração de um produto em uma colmeia               |

---

### Health Service (`/health`)

| Método | Rota      | Descrição                                                        |
| :----- | :-------- | :--------------------------------------------------------------- |
| `GET`  | `/health` | Verifica a integridade da API, conexões com PostgreSQL e MongoDB |

---

## Endpoints do Serviço de ML (Porta 8001)

O microserviço de ML aceita conexões protegidas por um token secreto no cabeçalho HTTP:
`X-ML-Service-Token: <ML_SERVICE_TOKEN>`

| Método | Rota       | Descrição                                                                                              |
| :----- | :--------- | :----------------------------------------------------------------------------------------------------- |
| `POST` | `/analyze` | Recebe `inspection_id` e a imagem em Base64, criando a tarefa no Celery/Redis. Retorna `202 Accepted`. |
| `GET`  | `/species` | Retorna a lista de espécies de abelhas sem ferrão suportadas pelo modelo treinado.                     |
| `GET`  | `/health`  | Status de saúde do serviço de ML e disponibilidade do Redis.                                           |

---

## Tratamento de Erros e Padrão de Resposta

Em caso de erros na API Principal, o sistema responde utilizando o padrão RFC 7807 com códigos HTTP semânticos:

- **`400 Bad Request`**: Dados inválidos, imagem vazia ou maior que 10MB.
- **`401 Unauthorized`**: Token JWT ausente ou expirado / Token de ML inválido.
- **`404 Not Found`**: Colmeia, inspeção ou foto não encontrada.
- **`429 Too Many Requests`**: Limite de taxa de requisições excedido.
- **`500 Internal Server Error`**: Erro não tratado no servidor.

Exemplo de resposta de erro:

```json
{
  "detail": "Imagem maior que 10MB"
}
```
