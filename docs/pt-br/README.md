# Melitrack - Documentação do Sistema (Português)

Bem-vindo à documentação oficial do **Melitrack**, uma plataforma inteligente e integrada para gestão de meliponários, monitoramento de abelhas sem ferrão (_Meliponini_), registro de colheitas, análises por Visão Computacional / Inteligência Artificial e observabilidade em tempo real.

---

## Navegação por Idioma

- 🇧🇷 **Documentação em Português** (Atual)
- 🇺🇸 [**English Documentation**](../en/README.md)

---

## Índice da Documentação

A documentação está dividida nos seguintes tópicos detalhados:

| Documento | Descrição |
| :--- | :--- |
| 🏗️ [**Arquitetura do Sistema**](ARCHITECTURE.md) | Visão geral dos microserviços, containerização, filas assíncronas e observabilidade. |
| 🗄️ [**Modelo de Banco de Dados**](DATABASE.md) | Detalhamento da arquitetura de dados híbrida (PostgreSQL + MongoDB) e diagrama ER. |
| 🔌 [**Serviços & APIs**](SERVICES_AND_API.md) | Especificação das rotas REST (FastAPI), autenticação JWT/OAuth, rate limit e pipeline de ML. |
| 🚀 [**Guia de Instalação e Execução**](SETUP_AND_RUN.md) | Passo a passo para rodar a aplicação via Docker Compose e configurar variáveis de ambiente. |

---

## Visão Geral do Projeto

O **Melitrack** foi desenvolvido para auxiliar meliponicultores no manejo eficiente de suas colmeias. A plataforma combina um frontend moderno e responsivo com uma arquitetura resiliente de microserviços no backend, permitindo:

- **Gestão de Colmeias**: Cadastro geolocalizado de caixas, espécies (_Jataí, Mandaçaia, Uruçu, Bugia, etc._), tipos de caixas (INPA, AF, etc.) e histórico fotográfico.
- **Inspeções Periódicas**: Registro de saúde da colônia, presença da rainha, estimativa de população, nível de mel e observações de campo.
- **Análise Inteligente por IA (ML)**: Processamento assíncrono de fotos das inspeções para identificação de espécies e avaliação da saúde da colônia através de visão computacional.
- **Controle de Colheitas e Produtos**: Rastreamento de produção de Mel, Própolis, Pólen, Geopropólis e Cera com métricas quantitativas.
- **Observabilidade em Tempo Real**: Coleta e centralização de logs e métricas do ecossistema via **Grafana, Loki e Grafana Alloy**.
