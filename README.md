# Ambiente NCA - Stack de Automação

Este projeto implementa um stack completo de automação e inteligência artificial, orquestrado com Docker Compose. Ele foi projetado para ser modular e extensível, fornecendo uma base sólida para a criação de fluxos de trabalho complexos.

## Visão Geral dos Serviços

O stack é composto pelos seguintes serviços:

- **n8n**: Plataforma de automação de fluxo de trabalho (workflow automation) que permite conectar diferentes APIs e serviços de forma visual.
- **MinIO**: Um serviço de armazenamento de objetos de alta performance compatível com a API do Amazon S3. Usado para armazenar arquivos, como os recebidos pelo nCA Toolkit.
- **Baserow**: Um banco de dados no-code de código aberto. Funciona como uma alternativa ao Airtable, usado aqui para registrar logs e outros dados estruturados.
- **Kokoro TTS**: Um serviço customizável de Text-to-Speech (TTS) para conversão de texto em voz.
- **nCA Toolkit**: Uma API customizada em Flask que serve como um conjunto de ferramentas, integrando-se com os outros serviços para fornecer endpoints para IA (Ollama), upload de arquivos (MinIO) e logging (Baserow).

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em sua máquina:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o ambiente.

### 1. Clonar o Repositório

```bash
git clone <url-do-seu-repositorio>
cd ambiente-nca
```

### 2. Configurar as Variáveis de Ambiente

Este projeto utiliza um arquivo `.env` para gerenciar as configurações e segredos. Um arquivo de exemplo é fornecido.

Copie o arquivo de exemplo para criar seu arquivo de configuração local:

```bash
cp .env.example .env
```

Agora, **edite o arquivo `.env`** e preencha as variáveis, especialmente as seguintes:

- `BASEROW_API_KEY`: Sua chave de API gerada no Baserow.
- `BASEROW_TABLE_ID`: O ID da tabela no Baserow onde os logs serão armazenados.
- `N8N_BASIC_AUTH_USER` e `N8N_BASIC_AUTH_PASSWORD`: Credenciais para proteger sua instância do n8n.
- `MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD`: Credenciais de administrador para o MinIO.

### 3. Iniciar os Serviços

Com o arquivo `.env` configurado, inicie todos os serviços com o Docker Compose. O comando a seguir irá construir as imagens customizadas (se necessário) e iniciar todos os contêineres em modo detached (-d).

```bash
docker-compose up -d --build
```

Pode levar alguns minutos para que todos os serviços estejam totalmente operacionais, especialmente o Baserow na primeira execução.

## Acesso aos Serviços

Após a inicialização, os serviços estarão disponíveis nos seguintes endereços (considerando as portas padrão definidas no `.env.example`):

- **n8n**: `http://localhost:5680`
- **MinIO Console**: `http://localhost:9006`
- **Baserow**: `http://localhost:8081`
- **nCA Toolkit**: `http://localhost:8088`

## Uso do nCA Toolkit

A API do nCA Toolkit fornece os seguintes endpoints principais:

- `GET /`: Retorna uma mensagem de status e os endpoints disponíveis.
- `GET /health`: Endpoint de verificação de saúde, usado pelo Docker Compose.
- `POST /insight`: Envia um prompt para o serviço de IA (Ollama) e recebe uma resposta.
- `POST /upload`: Faz o upload de um arquivo para o MinIO.
- `POST /log`: Envia um payload JSON para ser registrado como uma nova linha no Baserow.

## Estrutura do Projeto

```
ambiente-nca/
├── kokoro/               # Código e Dockerfile para o serviço Kokoro TTS
├── nca-toolkit/          # Código e Dockerfile para o nCA Toolkit
├── .env.example          # Arquivo de exemplo para variáveis de ambiente
├── .gitignore            # Arquivos e diretórios ignorados pelo Git
├── docker-compose.yml    # Arquivo de orquestração dos serviços
└── README.md             # Esta documentação
```

## Gerenciamento dos Serviços

### Parar os serviços

Para parar todos os contêineres sem remover os dados:

```bash
docker-compose down
```

### Parar e remover os volumes de dados

Atenção: Este comando removerá permanentemente todos os dados armazenados nos volumes (fluxos do n8n, arquivos do MinIO, etc.).

```bash
docker-compose down --volumes
```

### Visualizar os logs

Para ver os logs de todos os serviços em tempo real:

```bash
docker-compose logs -f
```

Para ver os logs de um serviço específico (por exemplo, `nca-toolkit`):

```bash
docker-compose logs -f nca-toolkit
```

## Contribuições

Contribuições são bem-vindas. Para sugestões ou correções de bugs, por favor, abra uma issue ou envie um pull request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.