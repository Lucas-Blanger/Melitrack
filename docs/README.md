# Melitrack - Documentação do Sistema

Bem-vindo à documentação oficial do **Melitrack**, uma plataforma inteligente e integrada para gestão de meliponários, monitoramento de abelhas sem ferrão (_Meliponini_), registro de colheitas, análises por Visão Computacional / Inteligência Artificial e observabilidade em tempo real.

---

## Visão Geral do Projeto

O **Melitrack** foi desenvolvido para auxiliar meliponicultores no manejo eficiente de suas colmeias. A plataforma combina um frontend moderno e responsivo com uma arquitetura resiliente de microserviços no backend, permitindo:

- **Gestão de Colmeias**: Cadastro geolocalizado de caixas, espécies (_Jataí, Mandaçaia, Uruçu, Bugia, etc._), tipos de caixas (INPA, AF, etc.) e histórico fotográfico.
- **Inspeções Periódicas**: Registro de saúde da colônia, presença da rainha, estimativa de população, nível de mel e observações de campo.
- **Análise Inteligente por IA (ML)**: Processamento assíncrono de fotos das inspeções para identificação de espécies e avaliação da saúde da colônia através de visão computacional.
- **Controle de Colheitas e Produtos**: Rastreamento de produção de Mel, Própolis, Pólen, Geopropólis e Cera com métricas quantitativas.
- **Observabilidade em Tempo Real**: Coleta e centralização de logs e métricas do ecossistema via **Grafana, Loki e Grafana Alloy**.

---

## Índice da Documentação

A documentação está dividida nos seguintes tópicos detalhados:

| Documento                                                | Descrição                                                                                    |
| :------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| 🏗️ [**Arquitetura do Sistema**](ARCHITECTURE.md)         | Visão geral dos microserviços, containerização, filas assíncronas e observabilidade.         |
| 🗄️ [**Modelo de Banco de Dados**](DATABASE.md)           | Detalhamento da arquitetura de dados híbrida (PostgreSQL + MongoDB) e diagrama ER.           |
| 🔌 [**Serviços & APIs**](SERVICES_AND_API.md)            | Especificação das rotas REST (FastAPI), autenticação JWT/OAuth, rate limit e pipeline de ML. |
| 🚀 [**Guia de Instalação e Execução**](SETUP_AND_RUN.md) | Passo a passo para rodar a aplicação via Docker Compose e configurar variáveis de ambiente.  |

---

## Tecnologias Utilizadas

### Frontend

- **Framework**: [React 19](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [Vite](https://vitejs.dev/)
- **Estilização**: [Tailwind CSS](https://tailwindcss.com/)
- **Ícones**: [Lucide React](https://lucide.dev/)
- **Roteamento**: React Router DOM v7

### Backend API (Serviço Principal)

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12)
- **ORM & Migrações**: SQLAlchemy 2.0 + Alembic
- **Autenticação**: JWT (JSON Web Token) & Google OAuth2
- **Controle de Taxa**: Rate Limit Middleware customizado

### Backend ML (Serviço de Inteligência Artificial)

- **Framework**: FastAPI (Inferência) + [Celery](https://docs.celeryq.dev/) (Tarefas em segundo plano)
- **Message Broker / Cache**: [Redis 7](https://redis.io/)
- **Modelos**: TensorFlow / Keras (Visão Computacional) & Integração iNaturalist API

### Bancos de Dados & Armazenamento

- **PostgreSQL 16**: Armazenamento de dados relacionais estruturados (usuários, colmeias, inspeções, predições, colheitas).
- **MongoDB 8**: Banco de dados NoSQL focado no armazenamento binário de imagens e mídias das colmeias.

### Observabilidade & Infraestrutura

- **Logs & Monitoramento**: Grafana Alloy + Grafana Loki + Grafana Dashboards
- **Containerização**: Docker & Docker Compose com rede interna customizada (`melitrack-network`)

---

## Diagrama ER do Banco de Dados

O repositório inclui o diagrama de banco de dados oficial do sistema localizado em:
[`docs/melitrack_db .png`](melitrack_db%20.png)

Para mais detalhes sobre a estrutura das tabelas e coleções NoSQL, consulte o documento de [**Banco de Dados**](DATABASE.md).
