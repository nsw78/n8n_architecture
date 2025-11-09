# 📖 Guia do Pipeline de Geração de Conteúdo Automatizado

Este documento detalha o fluxo de trabalho completo para a geração de conteúdo multimídia (texto, imagem e vídeo) usando a stack do Ambiente NCA, orquestrado pelo n8n.

---

## ⚙️ Estrutura do Fluxo (n8n)

O pipeline é composto por 8 etapas sequenciais, cada uma executada por um nó específico no n8n.

### 🔹 1. Trigger Inicial

*   **Tipo de Nó**: `Cron` ou `Webhook`.
*   **Função**: Iniciar o processo.
    *   **Cron**: Agenda a execução para um horário específico (ex: diariamente às 08:00). É ideal para automação contínua.
    *   **Webhook**: Fornece uma URL que, ao ser chamada, inicia o fluxo. É ideal para integrações sob demanda.

### 🔹 2. Geração de Conteúdo (Texto com Ollama)

*   **Tipo de Nó**: `HTTP Request`.
*   **Função**: Gerar a narrativa principal do conteúdo.
*   **Configuração**:
    *   **Method**: `POST`
    *   **URL**: `http://nca-toolkit:8088/insight`
    *   **Body (JSON)**:
        ```json
        {
          "input": "Gere uma narrativa curta (máx. 100 palavras) sobre a crucificação de Jesus, estilo minimalista e melancólico, com tom reflexivo e esperançoso."
        }
        ```
*   **Saída**: Um objeto JSON contendo o texto gerado pela IA. Ex: `{ "response": "Nas trevas do Gólgota, o silêncio pesava..." }`.

### 🔹 3. Geração de Prompt Visual (Ollama novamente)

*   **Tipo de Nó**: `HTTP Request`.
*   **Função**: Criar um prompt otimizado para um modelo de geração de imagem, baseado no texto do passo anterior.
*   **Configuração**:
    *   **Method**: `POST`
    *   **URL**: `http://nca-toolkit:8088/insight`
    *   **Body (JSON com Expressão)**:
        ```json
        {
          "input": "Crie um prompt de imagem em inglês, detalhado e em estilo 'digital dark minimalista', baseado no seguinte texto: {{ $json.response }}"
        }
        ```
*   **Saída**: Um objeto JSON com o prompt para a imagem. Ex: `{ "response": "A minimalist digital painting, dark and melancholic tone, a single cross on a hill..." }`.

### 🔹 4. Geração da Imagem

*   **Tipo de Nó**: `HTTP Request`.
*   **Função**: Usar o prompt do passo 3 para gerar a imagem.
*   **Configuração**:
    *   **Method**: `POST`
    *   **URL**: A URL da API do seu serviço de imagem (ex: Stable Diffusion local, Leonardo.Ai, etc.).
    *   **Body**: O corpo da requisição dependerá da API escolhida, mas você usará o prompt gerado no passo 3.
    *   **Importante**: Configure o nó para receber o resultado como um **arquivo binário**.
*   **Saída**: O arquivo da imagem (`.png` ou `.jpg`).

### 🔹 5. Armazenamento da Imagem no MinIO

*   **Tipo de Nó**: `HTTP Request`.
*   **Função**: Fazer o upload da imagem binária para o MinIO.
*   **Configuração**:
    *   **Method**: `POST`
    *   **URL**: `http://nca-toolkit:8088/upload`
    *   **Body Content Type**: `Form-Data`
    *   **Mapeamento**: No campo `file`, selecione a saída binária do nó anterior (passo 4).
*   **Saída**: Um objeto JSON com a URL pública da imagem no MinIO.

### 🔹 6. Montagem do Vídeo (nCA Toolkit)

*   **Tipo de Nó**: `HTTP Request`.
*   **Função**: Orquestrar a criação do vídeo, combinando a imagem (passo 5) e o texto original (passo 2) para a narração.
*   **Configuração**:
    *   **Method**: `POST`
    *   **URL**: `http://nca-toolkit:8088/render`
    *   **Body (JSON com Expressões)**:
        ```json
        {
          "image_url": "{{ $node['Armazenamento da Imagem no MinIO'].json.url }}",
          "text": "{{ $node['Geração de Conteúdo (Texto com Ollama)'].json.response }}"
        }
        ```
*   **Saída**: Um objeto JSON com a URL do vídeo recém-criado no MinIO.

### 🔹 7. Armazenamento do Vídeo no MinIO

*   **Função**: Esta etapa já é **realizada automaticamente pelo endpoint `/render`** no passo 6. O `nca-toolkit` gera o vídeo e o envia diretamente para o MinIO, retornando a URL final. Portanto, um nó separado não é necessário.

### 🔹 8. Registro no Baserow

*   **Tipo de Nó**: `Baserow` (ou `HTTP Request` para o endpoint `/log`).
*   **Função**: Criar um registro completo de todo o conteúdo gerado, servindo como um log de produção.
*   **Configuração (Nó Baserow)**:
    *   **Operation**: `Create`
    *   **Table ID**: O ID da sua tabela no Baserow.
    *   **Fields (Mapeamento com Expressões)**:
        *   `Título`: (Você pode definir um título estático ou gerá-lo também).
        *   `Texto`: `{{ $node['Geração de Conteúdo (Texto com Ollama)'].json.response }}`
        *   `Prompt de Imagem`: `{{ $node['Geração de Prompt Visual'].json.response }}`
        *   `URL da Imagem`: `{{ $node['Armazenamento da Imagem no MinIO'].json.url }}`
        *   `URL do Vídeo`: `{{ $node['Montagem do Vídeo'].json.url }}`
        *   `Data de Geração`: `{{ $now }}`
*   **Saída**: Confirmação de que a linha foi criada no Baserow.

---

## ✅ Conclusão

Ao encadear esses 8 passos no n8n, você cria um pipeline totalmente automatizado que transforma uma única ideia (o prompt inicial) em um conteúdo multimídia completo (texto, imagem e vídeo), com tudo devidamente armazenado e catalogado.