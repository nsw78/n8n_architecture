# 📖 Documentação do `docker-compose.yml` - Ambiente NCA

Este documento fornece uma análise detalhada do arquivo `docker-compose.yml` do projeto **Ambiente NCA**. Ele descreve cada serviço, as configurações de rede, a persistência de dados e os comandos para gerenciar a stack.

---

## 1. Visão Geral

O `docker-compose.yml` orquestra um ecossistema de serviços para automação e geração de conteúdo com Inteligência Artificial. A arquitetura é modular, onde cada contêiner possui uma responsabilidade única, comunicando-se através de uma rede interna segura.

---

## 2. Estrutura de Serviços

A stack é composta pelos seguintes 8 serviços:

### 🧠 Serviços de Inteligência e Lógica

#### `nca-toolkit`
-   **Imagem**: Construída a partir de `./nca-toolkit`.
-   **Função**: O cérebro da operação. É uma API Flask customizada que atua como um maestro, recebendo requisições do `n8n` e coordenando as chamadas para os outros serviços (`Ollama`, `Kokoro`, `MinIO`, `Baserow`).
-   **Porta Exposta**: `8088`.
-   **Dependências**: Depende de quase todos os outros serviços para funcionar.

#### `ollama`
-   **Imagem**: `ollama/ollama:latest`.
-   **Função**: Fornece a capacidade de executar Modelos de Linguagem Grandes (LLMs) localmente. É o serviço responsável por gerar textos, insights e prompts.
-   **Porta Exposta**: `11434`.
-   **Persistência**: O volume `ambiente-nca_ollama_data` armazena os modelos de IA baixados.

#### `kokoro`
-   **Imagem**: Construída a partir de `./kokoro`.
-   **Função**: Serviço de Text-to-Speech (TTS). Converte os textos gerados pelo `Ollama` em arquivos de áudio (narrações).
-   **Porta Exposta**: `5002`.
-   **Persistência**: O volume `ambiente-nca_kokoro_data` armazena os modelos de voz.

### ⚙️ Serviços de Orquestração e Banco de Dados

#### `n8n`
-   **Imagem**: `n8nio/n8n:latest`.
-   **Função**: Ferramenta de automação de fluxos de trabalho (workflow). É usada para criar, agendar e executar o pipeline completo de geração de conteúdo de forma visual.
-   **Porta Exposta**: `5680`.
-   **Dependências**: Utiliza o serviço `postgres` como seu banco de dados.

#### `baserow`
-   **Imagem**: `baserow/baserow:latest`.
-   **Função**: Plataforma de banco de dados No-Code. Atua como um "Google Sheets" superpoderoso, usado para registrar e catalogar todo o conteúdo gerado pelo pipeline (textos, prompts, URLs de arquivos, etc.).
-   **Porta Exposta**: `8081`.
-   **Persistência**: Os dados são armazenados no volume `ambiente-nca_baserow_data`.
-   **Dependências**: Utiliza o serviço `postgres` como seu banco de dados.

#### `postgres`
-   **Imagem**: `postgres:15`.
-   **Função**: Banco de dados relacional robusto que serve como a base de dados persistente para os serviços `n8n` e `baserow`.
-   **Porta Exposta**: Nenhuma (acesso apenas pela rede interna).
-   **Persistência**: Os dados são armazenados no volume `ambiente-nca_postgres_data`.

### 🗄️ Serviços de Armazenamento e Backup

#### `minio`
-   **Imagem**: `minio/minio:latest`.
-   **Função**: Sistema de armazenamento de objetos compatível com a API S3 da Amazon. É usado para guardar todos os ativos digitais gerados, como imagens, áudios e vídeos.
-   **Portas Expostas**:
    -   `9005`: Porta da API S3 (para acesso programático).
    -   `9006`: Porta do Console Web (para gerenciamento manual).
-   **Persistência**: Os objetos são armazenados no volume `ambiente-nca_minio_data`.

#### `backup`
-   **Imagem**: `alpine:latest`.
-   **Função**: Um contêiner leve que executa um script (`/scripts/backup_volumes.sh`) em um loop diário para criar cópias de segurança compactadas dos volumes de dados (`postgres`, `minio`, `baserow`) e salvá-las no diretório local `./backup`.
-   **Acesso a Volumes**: Monta os volumes dos outros serviços em modo somente leitura (`:ro`) para garantir a segurança durante a cópia.

---

## 3. Configurações Globais

### `networks`
-   **`nca_network`**: Uma rede do tipo `bridge` customizada. Todos os serviços são conectados a esta rede, o que permite que eles se comuniquem uns com os outros usando seus nomes de serviço como hostname (ex: `http://postgres:5432`). Isso cria um ambiente de comunicação isolado e seguro.

### `volumes`
-   **`ambiente-nca_*_data`**: Volumes nomeados gerenciados pelo Docker. Eles são usados para persistir os dados de cada serviço (`postgres`, `minio`, `baserow`, `ollama`, `kokoro`), garantindo que as informações não sejam perdidas quando os contêineres são recriados ou atualizados.

---

## 4. Como Gerenciar o Ambiente

Todos os comandos devem ser executados no diretório raiz do projeto (`/home/nelsons_walcow/ambiente-nca/`).

-   **Subir todos os serviços em background:**
    ```bash
    docker compose up -d
    ```

-   **Subir e reconstruir as imagens customizadas (`nca-toolkit`, `kokoro`):**
    ```bash
    docker compose up -d --build
    ```

-   **Parar todos os serviços:**
    ```bash
    docker compose down
    ```

-   **Parar e remover os volumes (ATENÇÃO: todos os dados serão perdidos):**
    ```bash
    docker compose down -v
    ```

-   **Ver os logs de todos os serviços em tempo real:**
    ```bash
    docker compose logs -f
    ```

-   **Ver os logs de um serviço específico (ex: `nca-toolkit`):**
    ```bash
    docker compose logs -f nca-toolkit
    ```

-   **Recriar um serviço específico após uma alteração (ex: `nca-toolkit`):**
    ```bash
    docker compose up -d --force-recreate --build nca-toolkit
    ```
