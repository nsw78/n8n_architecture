
# 🚀 Ambiente NCA — Stack de Automação e Inteligência Artificial

O **Ambiente NCA** é uma stack completa de **automação**, **integração de serviços** e **inteligência artificial**, orquestrada com **Docker Compose**.  
Foi projetada para ser **modular, extensível e independente**, fornecendo uma base sólida para criação de **pipelines inteligentes**, APIs integradas e fluxos de trabalho complexos.

---

## 🧩 Visão Geral dos Serviços

| Serviço | Descrição |
|----------|------------|
| **🧠 nCA Toolkit** | API customizada em Flask que integra IA (Ollama), upload de arquivos (MinIO) e logging (Baserow). |
| **⚙️ n8n** | Plataforma de automação de fluxos (workflow automation) com interface visual para orquestrar APIs e serviços. |
| **🗄️ MinIO** | Armazenamento de objetos de alta performance, compatível com a API S3 da AWS. |
| **🧩 Baserow** | Banco de dados no-code de código aberto (alternativa ao Airtable), usado para logs e dados estruturados. |
| **🔊 Kokoro TTS** | Serviço de Text-to-Speech customizado para conversão de texto em voz. |
| **🤖 Ollama** | Executor local de modelos de linguagem (LLMs), integrado via API REST. |

---

## 🧱 Estrutura do Projeto

```

ambiente-nca/
├── kokoro/               # Serviço de TTS (Kokoro)
├── nca-toolkit/          # API Flask e integrações centrais
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore            # Padrões de exclusão do Git
├── docker-compose.yml    # Orquestração dos serviços
└── README.md             # Esta documentação

````

---

## ⚙️ Pré-requisitos

Certifique-se de ter os seguintes pacotes instalados:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🧭 Instalação e Configuração

### 1️⃣ Clonar o repositório

```bash
git clone <url-do-seu-repositorio>
cd ambiente-nca
````

### 2️⃣ Configurar variáveis de ambiente

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e defina as seguintes variáveis:

| Variável                                          | Descrição                |
| ------------------------------------------------- | ------------------------ |
| `BASEROW_API_KEY`                                 | Chave de API do Baserow  |
| `BASEROW_TABLE_ID`                                | ID da tabela para logs   |
| `N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD` | Credenciais do n8n       |
| `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`         | Usuário e senha do MinIO |

---

### 3️⃣ Iniciar os serviços

```bash
docker-compose up -d --build
```

> 💡 A primeira inicialização pode demorar alguns minutos, especialmente na configuração do Baserow.

---

## 🌐 Acesso aos Serviços

| Serviço               | URL                                              | Porta | Descrição                    |
| --------------------- | ------------------------------------------------ | ----- | ---------------------------- |
| 🧠 **nCA Toolkit**    | [http://localhost:8088](http://localhost:8088)   | 8088  | API principal (Flask)        |
| ⚙️ **n8n**            | [http://localhost:5680](http://localhost:5680)   | 5680  | Painel visual de automação   |
| 🔊 **Kokoro TTS**     | [http://localhost:5002](http://localhost:5002)   | 5002  | Conversão texto → voz        |
| 🗄️ **MinIO Console** | [http://localhost:9006](http://localhost:9006)   | 9006  | Interface web administrativa |
| 📦 **MinIO API (S3)** | [http://localhost:9005](http://localhost:9005)   | 9005  | Endpoint S3 para SDKs/CLI    |
| 🧩 **Baserow**        | [http://localhost:8081](http://localhost:8081)   | 8081  | Banco de dados visual        |
| 🤖 **Ollama (LLM)**   | [http://localhost:11434](http://localhost:11434) | 11434 | API REST para modelos locais |

> Se for acessar de outro dispositivo na rede, substitua `localhost` pelo IP do servidor.

---

## 🧠 Endpoints Principais do nCA Toolkit

| Método          | Endpoint                                            | Descrição |
| --------------- | --------------------------------------------------- | --------- |
| `GET /`         | Retorna status e endpoints disponíveis              |           |
| `GET /health`   | Verificação de saúde (health check)                 |           |
| `POST /insight` | Envia prompt para o Ollama e retorna resposta da IA |           |
| `POST /upload`  | Upload de arquivos para o MinIO                     |           |
| `POST /log`     | Registra logs ou eventos no Baserow                 |           |

---

## 🧩 Gerenciamento dos Serviços

### Parar todos os containers

```bash
docker-compose down
```

### Parar e remover volumes (⚠️ apaga dados)

```bash
docker-compose down --volumes
```

### Visualizar logs em tempo real

```bash
docker-compose logs -f
```

Ou para um serviço específico:

```bash
docker-compose logs -f nca-toolkit
```

---

## 🤝 Contribuições

Contribuições são **muito bem-vindas**!
Abra uma *issue* para sugestões, relatórios de bug ou novas ideias — ou envie um *pull request* diretamente.

---

## 📄 Licença

Distribuído sob a **Licença MIT**.
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

### ✨ Autor

**Nelson dos Santos Walcow**
Especialista em Cloud, SRE, DevOps e Arquitetura de Infraestrutura
🌐 [LinkedIn](https://www.linkedin.com) • 🐙 [GitHub](https://github.com/nsw78)


