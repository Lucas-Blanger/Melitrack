# Modelo de Banco de Dados - Melitrack

O **Melitrack** adota uma estratégia de armazenamento **poliglota (híbrida)**, combinando a integridade relacional do **PostgreSQL** para a regra de negócio central com a alta performance NoSQL do **MongoDB** para o armazenamento binário e mídias fotográficas.

---

## Diagrama de Banco de Dados

O diagrama oficial de entidade-relacionamento (ER) do projeto está disponível em:
[**Visualizar Diagrama do Banco de Dados**](melitrack_db%20.png)

![Diagrama do Banco de Dados Melitrack](melitrack_db%20.png)

---

## 1. Banco Relacional (PostgreSQL)

O **PostgreSQL 16** é utilizado via ORM **SQLAlchemy 2.0** com controle de versões de esquema via **Alembic**.

### Tipos Enumerados (Enums)

- **`HiveType`**:
  - `inpa`: Caixa no padrão INPA (Módulos de Ninho, Sobre-ninho, Melgueira).
  - `af`: Caixa no padrão AF (AF-1 / AF-2).
  - `troncofixo`: Racionalização ou tronco natural.
  - `outro`: Outros modelos artesanais ou caixas customizadas.

- **`ColonyHealth`**:
  - `excelente`: Colônia muito forte, alimento abundante e postura perfeita.
  - `boa`: Colônia saudável em desenvolvimento regular.
  - `alerta`: Sinais de fragilidade, ataque de forídeos ou escassez de alimento.
  - `critica`: Risco iminente de colapso ou abandono da caixa.

- **`AnalysisStatus`**:
  - `pending`: Análise de visão computacional enfileirada ou aguardando processamento.
  - `processing`: Análise sendo executada pelo Celery Worker.
  - `completed`: Predição concluída com sucesso.
  - `failed`: Falha no processamento da imagem ou formato inválido.
  - `corrected`: Resultado da IA ajustado manualmente pelo meliponicultor.

---

### Tabelas do PostgreSQL

#### 1. `users` (Usuários do Sistema)

Armazena as contas dos meliponicultores, credenciais de acesso e preferências do meliponário.

| Coluna                      | Tipo          | Restrições                   | Descrição                                    |
| :-------------------------- | :------------ | :--------------------------- | :------------------------------------------- |
| `id`                        | `UUID`        | PK, Default: `uuid4()`       | Identificador único do usuário               |
| `name`                      | `VARCHAR`     | NOT NULL                     | Nome completo                                |
| `email`                     | `VARCHAR`     | NOT NULL, UNIQUE, INDEX      | E-mail de login                              |
| `hashed_password`           | `VARCHAR`     | NOT NULL                     | Senha criptografada (Bcrypt)                 |
| `is_active`                 | `BOOLEAN`     | Default: `true`              | Status da conta                              |
| `auth_provider`             | `VARCHAR`     | NOT NULL, Default: `'local'` | Provedor de autenticação (`local`, `google`) |
| `google_id`                 | `VARCHAR`     | UNIQUE, NULLABLE             | ID do perfil Google                          |
| `picture`                   | `VARCHAR`     | NULLABLE                     | URL da foto de perfil                        |
| `reset_code`                | `VARCHAR`     | NULLABLE                     | Código para recuperação de senha             |
| `reset_code_expires`        | `TIMESTAMPTZ` | NULLABLE                     | Expiração do código de recuperação           |
| `meliponary_name`           | `VARCHAR`     | Default: `'Meu Meliponário'` | Nome personalizado do meliponário            |
| `meliponary_location`       | `VARCHAR`     | NULLABLE                     | Localização geral do meliponário             |
| `inspection_frequency_days` | `INTEGER`     | Default: `14`                | Frequência sugerida para inspeções (dias)    |
| `notify_health_alerts`      | `BOOLEAN`     | Default: `true`              | Notificar alertas de saúde                   |
| `notify_email`              | `BOOLEAN`     | Default: `true`              | Receber notificações por e-mail              |
| `created_at` / `updated_at` | `TIMESTAMPTZ` | Default: `now()`             | Timestamp de auditoria                       |

---

#### 2. `hives` (Colmeias)

Armazena as caixas racionais cadastradas pelo usuário.

| Coluna                      | Tipo             | Restrições                        | Descrição                                        |
| :-------------------------- | :--------------- | :-------------------------------- | :----------------------------------------------- |
| `id`                        | `UUID`           | PK, Default: `uuid4()`            | ID único da colmeia                              |
| `owner_id`                  | `UUID`           | FK -> `users.id`, NOT NULL, INDEX | Proprietário da colmeia                          |
| `name`                      | `VARCHAR(150)`   | NOT NULL                          | Nome ou identificador da caixa (ex: _Jataí-01_)  |
| `type`                      | `ENUM(HiveType)` | NOT NULL                          | Modelo da caixa (`inpa`, `af`, etc.)             |
| `species`                   | `VARCHAR(100)`   | NOT NULL                          | Nome da espécie (_Tetragonisca angustula_, etc.) |
| `latitude`                  | `FLOAT`          | NULLABLE                          | Coordenada GPS (Latitude)                        |
| `longitude`                 | `FLOAT`          | NULLABLE                          | Coordenada GPS (Longitude)                       |
| `location_description`      | `VARCHAR(255)`   | NULLABLE                          | Descrição do local (ex: _Próximo ao pomar_)      |
| `notes`                     | `TEXT`           | NULLABLE                          | Anotações adicionais                             |
| `created_at` / `updated_at` | `TIMESTAMPTZ`    | Default: `now()`                  | Timestamps                                       |

---

#### 3. `inspections` (Inspeções de Manejo)

Registros de verificações periódicas realizadas nas colmeias.

| Coluna                | Tipo                 | Restrições                                  | Descrição                                          |
| :-------------------- | :------------------- | :------------------------------------------ | :------------------------------------------------- |
| `id`                  | `UUID`               | PK, Default: `uuid4()`                      | ID único da inspeção                               |
| `hive_id`             | `UUID`               | FK -> `hives.id` (ON DELETE CASCADE), INDEX | Colmeia inspecionada                               |
| `owner_id`            | `UUID`               | FK -> `users.id`, INDEX                     | Proprietário                                       |
| `health`              | `ENUM(ColonyHealth)` | NOT NULL                                    | Avaliação de saúde da colônia                      |
| `queen_seen`          | `BOOLEAN`            | NULLABLE                                    | Avistamento da rainha                              |
| `honey_level`         | `INTEGER`            | NULLABLE                                    | Estimativa de mel (escala 1 a 5)                   |
| `population_estimate` | `VARCHAR(50)`        | NULLABLE                                    | Estimativa populacional (_baixa_, _média_, _alta_) |
| `notes`               | `TEXT`               | NULLABLE                                    | Observações registradas durante o manejo           |
| `inspected_at`        | `TIMESTAMPTZ`        | Default: `now()`                            | Data e hora da inspeção                            |

---

#### 4. `ml_predictions` (Resultados de Inteligência Artificial)

Predições de visão computacional associadas a uma inspeção.

| Coluna             | Tipo                   | Restrições                               | Descrição                                       |
| :----------------- | :--------------------- | :--------------------------------------- | :---------------------------------------------- |
| `id`               | `UUID`                 | PK, Default: `uuid4()`                   | ID único do registro de ML                      |
| `inspection_id`    | `UUID`                 | FK -> `inspections.id`, UNIQUE, NOT NULL | Inspeção vinculada (Relação 1-para-1)           |
| `status`           | `ENUM(AnalysisStatus)` | Default: `'pending'`                     | Status do processamento da IA                   |
| `model_name`       | `VARCHAR(100)`         | NULLABLE                                 | Nome/Versão do modelo utilizado                 |
| `result`           | `JSONB`                | NULLABLE                                 | Resultado da inferência (espécie, score, saúde) |
| `confidence`       | `FLOAT`                | NULLABLE                                 | Nível de confiança do modelo (0.0 a 1.0)        |
| `error_message`    | `TEXT`                 | NULLABLE                                 | Mensagem de erro em caso de falha no Celery     |
| `corrected_result` | `JSONB`                | NULLABLE                                 | Resultado corrigido manualmente pelo usuário    |
| `correction_notes` | `TEXT`                 | NULLABLE                                 | Motivo/Observação da correção                   |
| `corrected_at`     | `TIMESTAMPTZ`          | NULLABLE                                 | Data da correção manual                         |
| `processed_at`     | `TIMESTAMPTZ`          | NULLABLE                                 | Data/Hora de conclusão do processamento pela IA |

---

#### 5. `products` (Produtos da Meliponicultura)

Catálogo de produtos derivados das abelhas.

| Coluna        | Tipo           | Restrições        | Descrição                                            |
| :------------ | :------------- | :---------------- | :--------------------------------------------------- |
| `id`          | `SERIAL`       | PK, Autoincrement | ID do produto                                        |
| `name`        | `VARCHAR(100)` | UNIQUE, NOT NULL  | Nome do produto (_Mel_, _Própolis_, _Cera_, _Pólen_) |
| `unit`        | `VARCHAR(20)`  | NOT NULL          | Unidade padrão (`ml`, `g`, `kg`)                     |
| `description` | `TEXT`         | NULLABLE          | Descrição do produto                                 |
| `is_active`   | `BOOLEAN`      | Default: `true`   | Status ativo no catálogo                             |

---

#### 6. `harvests` (Registros de Colheita)

Lançamento de colheitas efetuadas nas colmeias.

| Coluna          | Tipo          | Restrições              | Descrição                         |
| :-------------- | :------------ | :---------------------- | :-------------------------------- |
| `id`            | `UUID`        | PK, Default: `uuid4()`  | ID único da colheita              |
| `hive_id`       | `UUID`        | FK -> `hives.id`, INDEX | Colmeia de origem                 |
| `owner_id`      | `UUID`        | FK -> `users.id`        | Proprietário                      |
| `product_id`    | `INTEGER`     | FK -> `products.id`     | Produto colhido                   |
| `quantity`      | `FLOAT`       | NOT NULL                | Quantidade colhida                |
| `unit`          | `VARCHAR(20)` | NOT NULL                | Unidade de medida                 |
| `quality_notes` | `TEXT`        | NULLABLE                | Notas sobre cor, sabor ou umidade |
| `harvested_at`  | `TIMESTAMPTZ` | Default: `now()`        | Data da extração                  |

---

## 2. Banco NoSQL (MongoDB)

O **MongoDB 8** é acessado de forma totalmente assíncrona através da biblioteca **Motor**. Ele é responsável por armazenar as fotos enviadas pelos usuários em formato binário (`bytes`) evitando o sobrecarregamento do banco relacional.

### Coleção: `hive_photos`

Armazena fotos gerais da caixa ou estrutura do meliponário.

```json
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d0"),
  "owner_id": "uuid-string-do-usuario",
  "hive_id": "uuid-string-da-colmeia",
  "filename": "foto_caixa.jpg",
  "content_type": "image/jpeg",
  "size": 2450800,
  "data": Binary(Buffer),
  "uploaded_at": ISODate("2026-09-04T12:00:00Z")
}
```

### Coleção: `inspection_photos`

Armazena fotos internas tiradas durante a inspeção e enviadas para análise de ML.

```json
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d1"),
  "owner_id": "uuid-string-do-usuario",
  "hive_id": "uuid-string-da-colmeia",
  "inspection_id": "uuid-string-da-inspecao",
  "filename": "favo_postura.jpg",
  "content_type": "image/jpeg",
  "size": 1820400,
  "data": Binary(Buffer),
  "uploaded_at": ISODate("2026-09-04T12:05:00Z"),
  "ml_status": "pending"
}
```

> **Nota de Design**: Nas respostas da API REST (`PhotoResponse`), o campo `data` binário armazena o arquivo e é convertido dinamicamente em uma URL no formato Data URI (`data:image/jpeg;base64,...`) para renderização direta nas tags `<img>` do frontend React sem necessidade de servidores de mídia externos adicionais.
