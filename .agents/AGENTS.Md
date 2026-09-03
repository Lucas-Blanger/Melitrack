# Contexto do Projeto

O **Melitrack** é uma plataforma de monitoramento, rastreamento e classificação de abelhas e insetos utilizando Machine Learning.
Este repositório é monorepo e contém os seguintes componentes:
- **Backend API**: API REST principal em Python (FastAPI), PostgreSQL e MongoDB (`backend/api/`).
- **Backend ML**: Serviço de Machine Learning com TensorFlow, FastAPI e Celery + Redis (`backend/ml/`).
- **Frontend**: Aplicação web SPA em React com Vite e Tailwind CSS (`frontend/`).
- **Orquestração e Observabilidade**: Manifestos nativos Kubernetes (`k8s/`), Docker Compose e stack Grafana/Loki/Alloy (`observability/`).

Antes de iniciar qualquer tarefa, leia o código e as configurações relacionadas ao módulo que será alterado.

---

# Regras de Trabalho e Arquitetura

- **Passos incrementais**: Trabalhar em etapas pequenas e verificáveis.
- **Escopo estrito**: Implementar SOMENTE o que foi solicitado. Não adicionar funcionalidades extras.
- **Reutilização**: Maximizar a reutilização de código existente. Não reescrever soluções funcionais.
- **Isolamento**: Não alterar módulos ou arquivos que não estejam diretamente relacionados à tarefa.
- **Design Modular**:
  - `backend/api/apps/`: Rotas, schemas Pydantic e lógica de negócio dos recursos da API principal.
  - `backend/ml/app/`: Tarefas de inferência, processamento Celery e integração com iNaturalist.
  - `frontend/src/`: Componentes funcionais React, hooks customizados e chamadas de serviços centralizados.
- **Práticas de Código**:
  - **Python**: Utilizar Python 3.12+ moderno (`async/await`, type hints completos).
  - **JavaScript/TypeScript**: Utilizar ES6+ / TypeScript com `async/await`. NUNCA usar `.then()/.catch()`.
- **Segurança**: Não expor dados sensíveis (senhas, hashes, secret keys, tokens) nas respostas da API ou em arquivos públicos do repositório.
- **Idioma**: Escrever mensagens de erro, logs, comentários de código e documentação em português.

---

# Fluxo Antes de Alterar Código

1. **Leitura**: Ler o código e a arquitetura relacionada à tarefa.
2. **Padrões**: Identificar os padrões de código e design existentes no arquivo/módulo.
3. **Planejamento**: Apresentar um plano curto e objetivo da implementação ao usuário.
4. **Autorização**: Aguardar a autorização do usuário antes de realizar alterações estruturais significativas.
5. **Execução**: Implementar estritamente a etapa solicitada.
6. **Revisão**: Revisar as alterações e informar os arquivos modificados.

---

# Testes e Qualidade

- Toda nova regra de negócio deve possuir teste automatizado quando aplicável.
- Dar preferência a testes simples e focados (Testes unitários com `pytest` no backend).
- Não remover ou enfraquecer testes existentes para fazer a implementação passar.
- Antes de concluir uma etapa, executar a suíte de testes configurada:
  - Backend API: `pytest` na pasta `backend/api/`
  - Backend ML: `pytest` na pasta `backend/ml/`
  - Frontend: `npm test` ou `npm run build` na pasta `frontend/`

---

# Git e Commits

- Não executar comandos Git que criem ou enviem commits (`git commit`, `git push`) a menos que explicitamente solicitado pelo usuário.

---

# Limites de Autonomia do Agente

### O Agente PODE:
- Ler arquivos e analisar a base de código do Melitrack;
- Modificar arquivos diretamente relacionados à tarefa atual;
- Criar e atualizar testes automatizados;
- Executar comandos locais de verificação, testes e build (ex: `pytest`, `npm run dev`, `kubectl apply --dry-run`);
- Apresentar sugestões técnicas e arquiteturais.

### O Agente NÃO PODE (sem autorização explícita):
- Fazer push para o repositório remoto;
- Criar ou enviar commits no Git;
- Apagar migrações de banco de dados (`alembic/versions`);
- Adicionar novas dependências (`pip install`, `npm install`) sem necessidade comprovada;
- Fazer grandes refatorações estruturais em múltiplos módulos ao mesmo tempo;
- Executar comandos que destruam volumes ou quebrem o ambiente Docker/Kubernetes.

---

# Finalização de Cada Tarefa

Ao concluir uma instrução, o agente deve obrigatoriamente informar:

1. **O que foi implementado**.
2. **Quais arquivos foram criados ou alterados** (com links no formato `file:///caminho`).
3. **Quais decisões técnicas foram tomadas** (se houver).
4. **Se existe alguma pendência**.

Depois disso, parar imediatamente e aguardar novas instruções do usuário.
