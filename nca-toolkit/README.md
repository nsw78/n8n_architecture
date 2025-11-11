
# nCA Toolkit

## Visão Geral

O **nCA Toolkit** é um microserviço central do ecossistema **ambiente-nca**, desenvolvido em **Flask** para fornecer serviços de geração de insights com IA, armazenamento de arquivos e registro estruturado de dados.  

Ele integra-se com os serviços **Ollama**, **MinIO**, **Baserow** e **n8n**, formando uma pipeline automatizada e completa para geração e persistência de conteúdos inteligentes.  
O objetivo do toolkit é ser o núcleo de inteligência e integração de dados dentro do ambiente distribuído, oferecendo endpoints REST seguros e prontos para automação.

---

## Arquitetura do Ambiente

O projeto **ambiente-nca** é composto por múltiplos serviços containerizados, orquestrados via **Docker Compose**, conforme a tabela abaixo:

| Serviço | Descrição |
|----------|------------|
| **nca-toolkit** | Núcleo principal em Flask responsável pela comunicação com IA, upload de arquivos e logs estruturados. |
| **n8n** | Plataforma de automação que orquestra o pipeline de geração de insights. |
| **MinIO** | Armazenamento de objetos compatível com S3, usado para persistência de arquivos e resultados. |
| **PostgreSQL** | Banco de dados relacional utilizado por MinIO e Baserow. |
| **Baserow** | Banco de dados no-code para armazenamento de logs, registros e insights. |
| **Kokoro** | Serviço auxiliar responsável por processos de automação e renderização. |

---

## Principais Funcionalidades

- Geração de insights utilizando **Ollama**.  
- Pipeline de processamento automatizado orquestrado via **n8n**.  
- Upload e persistência de arquivos em **MinIO**.  
- Registro estruturado de logs e metadados no **Baserow**.  
- API REST segura e padronizada.  
- Monitoramento via health check interno.  
- Integração com automações externas e scripts dedicados.  
- Configuração e deploy totalmente containerizados.

---

## Estrutura do Projeto

```

ambiente-nca
├── baserow/                     # Banco de dados no-code para registros e logs
├── data/                        # Dados de referência (ex: a_luz_nas_trevas.json)
├── docs/
│   ├── detail.md                # Documentação técnica detalhada
│   └── workflow-pipeline.md     # Pipeline de automação (n8n → nca-toolkit → Ollama)
├── kokoro/                      # Serviço auxiliar de automação
│   └── Dockerfile
├── minio/                       # Armazenamento S3 compatível
├── n8n/                         # Automação de workflows e orquestração
├── nca-toolkit/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── main.py              # Ponto de entrada Flask
│   │   ├── config.py            # Configurações do ambiente
│   │   ├── services/
│   │   │   ├── ollama_client.py # Cliente de comunicação com o Ollama
│   │   │   ├── minio_client.py  # Cliente de integração com o MinIO
│   │   │   └── baserow_client.py# Cliente de integração com o Baserow
│   │   └── utils/
│   │       └── logger.py        # Configuração central de logs
│   └── tests/
│       └── test_main.py         # Testes unitários
├── scripts/
│   ├── create_baserow_table.py  # Script para criação automática de tabelas no Baserow
│   ├── data/
│   ├── kokoro/
│   │   └── models/
│   ├── logs/
│   ├── nca-toolkit/
│   │   └── src/
│   └── setup.sh                 # Script de configuração do ambiente
├── docker-compose.yml           # Orquestração dos serviços
├── README.md                    # Documentação principal

```

---

## Variáveis de Ambiente

O arquivo `.env` deve conter as variáveis abaixo:

```

FLASK_ENV=production
PORT=8088

# Ollama

OLLAMA_URL=[http://ollama:11434](http://ollama:11434)

# MinIO

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=nca-data

# Baserow

BASEROW_API_URL=[http://baserow:8000/api/database/rows/table/1](http://baserow:8000/api/database/rows/table/1)
BASEROW_TOKEN=seu_token_baserow

````

---

## Execução Local

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd nca-toolkit
````

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` conforme o ambiente.

5. Inicie o servidor Flask:

   ```bash
   python src/main.py
   ```

O serviço estará disponível em:
`http://localhost:8088`

---

## Execução via Docker

Para subir todos os serviços do ambiente nCA:

```bash
docker compose up -d
```

Verificar os containers em execução:

```bash
docker ps
```

Acompanhar logs do serviço principal:

```bash
docker logs ambiente-nca-nca-toolkit-1 --tail=50
```

---

## Endpoints da API

### 1. Health Check

**GET** `/health`
Verifica o status do serviço.

**Resposta:**

```json
{
  "status": "healthy",
  "service": "nca-toolkit"
}
```

---

### 2. Geração de Insight

**POST** `/insight`
Gera respostas inteligentes usando o modelo Ollama.

**Exemplo de Requisição:**

```json
{
  "prompt": "Explique o impacto da IA na computação em nuvem."
}
```

**Exemplo de Resposta:**

```json
{
  "insight": "A inteligência artificial está transformando a computação em nuvem ao permitir escalonamento preditivo..."
}
```

---

### 3. Upload de Arquivo

**POST** `/upload`
Realiza upload de arquivos para o MinIO.

**Form Data:**

```
file=<arquivo>
```

**Resposta:**

```json
{
  "filename": "exemplo.pdf",
  "url": "http://minio:9000/nca-data/exemplo.pdf"
}
```

---

### 4. Registro de Log

**POST** `/log`
Grava informações no Baserow.

**Exemplo de Requisição:**

```json
{
  "usuario": "admin",
  "acao": "gerar_insight",
  "timestamp": "2025-11-10T21:00:00Z"
}
```

**Resposta:**

```json
{
  "status": "success",
  "id": 42
}
```

---

## Pipeline de Geração de Insights Automatizada

O pipeline **n8n → nca-toolkit → Ollama → Baserow → MinIO** executa automaticamente o processo de criação, registro e armazenamento dos insights.

Fluxo resumido:

1. O **n8n** inicia o fluxo a partir de uma trigger (manual ou automatizada).
2. O **nca-toolkit** recebe a requisição e consulta o **Ollama** para gerar o insight.
3. O resultado é armazenado no **MinIO** (se houver arquivo) e registrado no **Baserow**.
4. O **kokoro** pode realizar pós-processamento ou renderização adicional conforme o contexto.
5. Todo o processo é logado e auditável.

Documentação detalhada: `docs/workflow-pipeline.md`

---

## Testes

Para executar os testes unitários:

```bash
pytest -v
```

---

## Contribuição

Contribuições são bem-vindas.
Antes de enviar um **pull request**, verifique se os testes estão passando e se a documentação está atualizada.

---

## Licença

Este projeto é licenciado sob os termos da **MIT License**.
Consulte o arquivo `LICENSE` para mais informações.


