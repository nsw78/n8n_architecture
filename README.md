
# Ambiente NCA — Stack de Automação e Inteligência Artificial

O **Ambiente NCA** é uma stack modular e integrada para **automação de processos**, **integração de serviços** e **inteligência artificial**, orquestrada por meio de **Docker Compose**.  
O ecossistema foi desenvolvido para fornecer uma base sólida e escalável de **pipelines inteligentes**, permitindo gerar, armazenar e catalogar conteúdo multimídia a partir de fluxos de dados dinâmicos.

A arquitetura combina processamento assíncrono, geração de insights por LLMs locais, integração com serviços REST, armazenamento S3 e automação de workflows.

---

## 1. Arquitetura Geral

| Serviço | Função | Descrição Técnica |
|----------|--------|-------------------|
| **n8n** | Orquestrador de Fluxos | Gerencia e executa workflows automatizados que disparam o pipeline de geração de conteúdo. |
| **nCA Toolkit** | API Central | Aplicação em Flask que integra e coordena os serviços da stack (Ollama, Kokoro, MinIO e Baserow). É o ponto de entrada para o processamento e registro de dados. |
| **Ollama** | Módulo de IA (LLM) | Responsável pela geração de texto e insights através de modelos de linguagem locais. |
| **Kokoro TTS** | Conversor de Texto em Áudio | Transforma o texto gerado em locuções de alta qualidade (Text-to-Speech). |
| **MinIO** | Armazenamento (S3-Compatible) | Serviço de armazenamento de objetos compatível com a API S3, utilizado para guardar os artefatos gerados. |
| **Baserow** | Catálogo e Registro | Banco de dados no-code que mantém o histórico de logs, URLs e metadados do conteúdo processado. |

---

## 2. Estrutura do Projeto

```

ambiente-nca/
├── baserow/                # Diretório do banco de dados Baserow
├── data/                   # Arquivos de dados (ex: JSONs de conteúdo)
│   └── a_luz_nas_trevas.json
├── docker-compose.yml      # Orquestração dos serviços
├── docs/                   # Documentação técnica detalhada
│   ├── detail.md
│   └── workflow-pipeline.md
├── kokoro/                 # Serviço de TTS
│   └── Dockerfile
├── minio/                  # Serviço de armazenamento S3
├── n8n/                    # Fluxos automatizados do orquestrador
├── nca-toolkit/            # API Flask central e integrações
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── services/
│   │   │   ├── baserow_client.py
│   │   │   ├── minio_client.py
│   │   │   └── ollama_client.py
│   │   └── utils/
│   │       └── logger.py
│   └── tests/
│       └── test_main.py
├── scripts/                # Scripts auxiliares e automações
│   ├── create_baserow_table.py
│   └── setup.sh
└── README.md               # Documentação principal

```

---

## 3. Fluxo de Processamento — Pipeline de Conteúdo Inteligente

O pipeline principal do **Ambiente NCA** foi projetado para automatizar a criação de conteúdo inteligente, conectando os serviços de IA, voz, armazenamento e registro.  
O fluxo ocorre da seguinte forma:

1. **Disparo (n8n)**  
   O processo inicia em um *workflow* do n8n, que envia uma requisição HTTP para o endpoint `/insight` do nCA Toolkit, contendo o prompt, parâmetros e contexto do conteúdo.

2. **Geração de Insight (nCA Toolkit + Ollama)**  
   O nCA Toolkit recebe a solicitação e comunica-se com o serviço Ollama, que processa o prompt através do modelo de linguagem (LLM) configurado e retorna um texto gerado.

3. **Conversão de Voz (Kokoro TTS)**  
   O texto é enviado ao serviço Kokoro, que o converte em áudio de alta qualidade, retornando um arquivo `.wav` ou `.mp3`.

4. **Armazenamento (MinIO)**  
   O áudio e demais artefatos (imagens, vídeos, metadados) são enviados para o MinIO, que atua como armazenamento S3 compatível, garantindo persistência e versionamento.

5. **Registro e Catálogo (Baserow)**  
   Ao final, o nCA Toolkit registra no Baserow todas as informações do pipeline — como URLs dos arquivos, data, tipo de conteúdo e metadados técnicos.

6. **Retorno ao Orquestrador**  
   O nCA Toolkit devolve ao n8n um objeto JSON consolidado com o resultado final do processamento, permitindo que o workflow continue (por exemplo, publicando o conteúdo gerado).

### Exemplo Simplificado de Fluxo

```

[Usuário/Evento] → n8n → nCA Toolkit → Ollama → Kokoro → MinIO → Baserow → [Retorno Final]

````

Cada etapa é registrada e auditável, permitindo rastreabilidade total de dados e outputs.

---

## 4. Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 5. Instalação e Configuração

### 5.1 Clonagem do Repositório

```bash
git clone <url-do-seu-repositorio>
cd ambiente-nca
````

### 5.2 Configuração das Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com os valores corretos para o seu ambiente.

| Variável                                          | Descrição                          |
| ------------------------------------------------- | ---------------------------------- |
| `BASEROW_API_KEY`                                 | Chave de autenticação do Baserow   |
| `BASEROW_TABLE_ID`                                | ID da tabela de logs               |
| `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`         | Credenciais do MinIO               |
| `N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD` | Credenciais de autenticação do n8n |

---

### 5.3 Inicialização dos Serviços

```bash
docker-compose up -d --build
```

A inicialização completa pode levar alguns minutos, especialmente na configuração inicial do Baserow.

---

## 6. Acesso aos Serviços

| Serviço                     | Endereço                                         | Porta | Descrição                             |
| --------------------------- | ------------------------------------------------ | ----- | ------------------------------------- |
| **nCA Toolkit (API Flask)** | [http://localhost:8088](http://localhost:8088)   | 8088  | API central da stack                  |
| **n8n (Orquestrador)**      | [http://localhost:5680](http://localhost:5680)   | 5680  | Automação visual e controle de fluxos |
| **Kokoro TTS**              | [http://localhost:5002](http://localhost:5002)   | 5002  | Conversão texto-voz                   |
| **MinIO Console**           | [http://localhost:9006](http://localhost:9006)   | 9006  | Interface administrativa              |
| **MinIO API (S3)**          | [http://localhost:9005](http://localhost:9005)   | 9005  | Endpoint compatível com S3            |
| **Baserow**                 | [http://localhost:8081](http://localhost:8081)   | 8081  | Banco no-code                         |
| **Ollama (LLM)**            | [http://localhost:11434](http://localhost:11434) | 11434 | API de modelos locais                 |

---

## 7. Endpoints Principais — nCA Toolkit

| Método               | Endpoint                                          | Descrição |
| -------------------- | ------------------------------------------------- | --------- |
| `GET /`              | Retorna status e endpoints disponíveis            |           |
| `GET /health`        | Health check do serviço                           |           |
| `POST /insight`      | Envia prompt ao Ollama e retorna resposta textual |           |
| `POST /upload`       | Upload de arquivos para o MinIO                   |           |
| `POST /log`          | Registro de eventos no Baserow                    |           |
| `POST /render`       | Gera vídeo ou áudio com base em texto e imagem    |           |
| `GET /data/timeline` | Retorna dados do arquivo `a_luz_nas_trevas.json`  |           |

---

## 8. Operações de Gerenciamento

### Parar os containers

```bash
docker-compose down
```

### Limpar volumes (remoção completa de dados)

```bash
docker-compose down --volumes
```

### Visualizar logs

```bash
docker-compose logs -f
```

Ou de um serviço específico:

```bash
docker-compose logs -f nca-toolkit
```

---

## 9. Diretrizes de Desenvolvimento

* Cada serviço é modular e comunica-se via REST.
* O log centralizado segue o padrão definido em `nca-toolkit/src/utils/logger.py`.
* Novas integrações devem ser registradas no `docker-compose.yml`.
* Testes unitários ficam em `nca-toolkit/tests/`.

---

## 10. Contribuições

Contribuições são bem-vindas.
Envie *issues* para sugestões e relatórios de bug ou *pull requests* com melhorias de código e documentação.

---

## 11. Licença

Distribuído sob a **Licença MIT**.
Consulte o arquivo `LICENSE` para mais informações.

---

## 12. Autor

**Nelson Walcow**
Especialista em Cloud, SRE, DevOps e Arquitetura de Infraestrutura
[LinkedIn](https://www.linkedin.com) • [GitHub](https://github.com/nsw78)


