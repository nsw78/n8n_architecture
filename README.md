
# Ambiente NCA — Stack de Automação e Inteligência Artificial

O **Ambiente NCA** é uma stack completa e modular para **automação de processos inteligentes**, **integração de IA local**, **armazenamento de ativos multimídia** e **gerenciamento de dados estruturados**.  
Projetado para uso profissional, o ambiente combina múltiplos serviços orquestrados por **Docker Compose**, criando uma infraestrutura totalmente integrada de processamento de dados e geração de conteúdo.

---

## 1. Arquitetura Geral

| Serviço | Porta | Endereço | Função | Descrição |
|----------|--------|-----------|---------|------------|
| **🧠 nCA Toolkit (Flask API)** | 8088 | [http://localhost:8088](http://localhost:8088) | Núcleo da stack | API principal, responsável por coordenar os fluxos entre IA, TTS, Baserow e MinIO. |
| **⚙️ n8n (Orquestrador)** | 5680 | [http://localhost:5680](http://localhost:5680) | Automação visual | Criação e execução de fluxos automatizados que disparam o pipeline de conteúdo. |
| **🔊 Kokoro TTS** | 5002 | [http://localhost:5002](http://localhost:5002) | Conversão texto-voz | Gera locuções de alta qualidade a partir de textos processados pelo LLM. |
| **🗄️ MinIO Console** | 9006 | [http://localhost:9006](http://localhost:9006) | Interface administrativa | Gerenciamento de objetos e buckets. |
| **📦 MinIO API (S3)** | 9005 | [http://localhost:9005](http://localhost:9005) | Endpoint S3 | Integração via SDKs e armazenamento programático. |
| **🧩 Baserow** | 8081 | [http://localhost:8081](http://localhost:8081) | Banco de dados visual | Registro e consulta de logs e metadados do pipeline. |
| **🐘 PostgreSQL** | 5432 | interno | Banco de dados relacional | Base persistente utilizada pelo Baserow. |
| **🤖 Ollama (LLM)** | 11434 | [http://localhost:11434](http://localhost:11434) | Módulo de IA | Modelo local de linguagem natural, responsável pela geração de texto e insights. |

---

## 2. Estrutura do Projeto

```

ambiente-nca/
├── baserow/                 # Banco de dados visual
├── data/                    # Arquivos JSON e conteúdos processados
│   └── a_luz_nas_trevas.json
├── docker-compose.yml       # Orquestração completa da stack
├── docs/
│   ├── detail.md
│   └── workflow-pipeline.md
├── kokoro/                  # Serviço TTS
│   └── Dockerfile
├── minio/                   # Configuração e volumes do MinIO
├── n8n/                     # Fluxos de automação
├── nca-toolkit/             # API Flask central
│   ├── src/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── services/
│   │   │   ├── ollama_client.py
│   │   │   ├── baserow_client.py
│   │   │   ├── minio_client.py
│   │   │   └── kokoro_client.py
│   │   └── utils/
│   │       └── logger.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       └── test_main.py
├── postgres/                # Volume persistente do PostgreSQL
├── scripts/
│   ├── create_baserow_table.py
│   └── setup.sh
└── README.md

```

---

## 3. Fluxo de Processamento — Pipeline de Conteúdo Inteligente

O **Ambiente NCA** utiliza uma arquitetura de integração total entre os serviços.  
O pipeline segue as seguintes etapas:

1. **Disparo do Workflow (n8n)**  
   Um fluxo do n8n envia um `POST` ao endpoint `/insight` do nCA Toolkit com o prompt e contexto.

2. **Geração de Texto (Ollama)**  
   O nCA Toolkit envia o prompt ao Ollama, que processa localmente com o modelo LLM configurado (por exemplo, `llama3` ou `mistral`).

3. **Conversão em Áudio (Kokoro TTS)**  
   O texto resultante é enviado ao Kokoro, que o transforma em arquivo de áudio `.wav` ou `.mp3`.

4. **Armazenamento (MinIO)**  
   O áudio e demais arquivos (textos, imagens, vídeos) são armazenados no MinIO — compatível com a API S3.

5. **Registro e Indexação (Baserow + PostgreSQL)**  
   O nCA Toolkit registra todos os metadados e URLs no Baserow, que utiliza o PostgreSQL como backend persistente.

6. **Retorno ao Orquestrador (n8n)**  
   O resultado final é devolvido em formato JSON, contendo os links de acesso aos arquivos no MinIO e os registros catalogados.

```

[Usuário/Evento] → n8n → nCA Toolkit → Ollama → Kokoro → MinIO → Baserow → PostgreSQL → [Retorno Final]

````

Essa arquitetura garante rastreabilidade, persistência e versionamento completo de cada item processado.

---

## 4. Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Recomendado: CPU Intel i5+ e 16GB RAM

---

## 5. Instalação e Configuração

### Clonagem

```bash
git clone <url-do-repositorio>
cd ambiente-nca
````

### Configuração de Variáveis

```bash
cp .env.example .env
```

Edite as credenciais conforme o ambiente:

| Variável                                          | Descrição                  |
| ------------------------------------------------- | -------------------------- |
| `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`         | Credenciais do MinIO       |
| `BASEROW_API_KEY`                                 | Token de acesso ao Baserow |
| `BASEROW_TABLE_ID`                                | ID da tabela de logs       |
| `N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD` | Login do painel n8n        |

---

## 6. Inicialização dos Serviços

```bash
docker compose up -d --build
```

Verifique os status de todos os containers:

```bash
docker ps
```

Esperado:

```
n8n                healthy
nca-toolkit        healthy
kokoro             healthy
minio              healthy
baserow            healthy
postgres           healthy
ollama             healthy
```

---

## 7. Endpoints do nCA Toolkit

| Método               | Endpoint                                | Descrição |
| -------------------- | --------------------------------------- | --------- |
| `GET /`              | Retorna status e documentação básica    |           |
| `GET /health`        | Verifica a saúde do serviço             |           |
| `POST /insight`      | Gera texto via Ollama                   |           |
| `POST /upload`       | Faz upload de arquivos para o MinIO     |           |
| `POST /log`          | Registra dados no Baserow               |           |
| `POST /render`       | Gera áudios ou vídeos baseados em texto |           |
| `GET /data/timeline` | Retorna dataset processado em JSON      |           |

---

## 8. Acesso aos Serviços

| Serviço                 | Endereço                                         | Porta |
| ----------------------- | ------------------------------------------------ | ----- |
| nCA Toolkit (API Flask) | [http://localhost:8088](http://localhost:8088)   | 8088  |
| n8n                     | [http://localhost:5680](http://localhost:5680)   | 5680  |
| Kokoro TTS              | [http://localhost:5002](http://localhost:5002)   | 5002  |
| MinIO Console           | [http://localhost:9006](http://localhost:9006)   | 9006  |
| MinIO API (S3)          | [http://localhost:9005](http://localhost:9005)   | 9005  |
| Baserow                 | [http://localhost:8081](http://localhost:8081)   | 8081  |
| Ollama (LLM)            | [http://localhost:11434](http://localhost:11434) | 11434 |

---

## 9. Operações Administrativas

### Parar containers

```bash
docker compose down
```

### Reiniciar com limpeza total

```bash
docker compose down -v
docker compose up -d --build
```

### Logs em tempo real

```bash
docker compose logs -f
```

---

## 10. Diagrama de Integração

```mermaid
graph TD
    A[n8n] --> B[nCA Toolkit]
    B --> C[Ollama (LLM)]
    B --> D[Kokoro TTS]
    B --> E[MinIO (S3 Storage)]
    E --> F[Baserow]
    F --> G[PostgreSQL]
    G -->|Persistência| F
    F -->|Retorno| B
    B -->|Output JSON| A
```

---

## 11. Diretrizes de Desenvolvimento

* Cada serviço comunica-se via REST.
* O log centralizado é padronizado no módulo `logger.py`.
* Novos endpoints devem ser documentados no `README` e registrados no `docker-compose.yml`.
* Testes automatizados em `nca-toolkit/tests/`.

---

## 12. Licença

Distribuído sob a **Licença MIT**.
Consulte o arquivo `LICENSE` para mais informações.

---

## 13. Autor

**Nelson Walcow**
Especialista em Cloud, SRE, DevOps e Arquitetura de Infraestrutura
[LinkedIn](https://www.linkedin.com) • [GitHub](https://github.com/nsw78)

