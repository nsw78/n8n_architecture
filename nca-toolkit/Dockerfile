# Estágio 1: Builder - Instala dependências de build e Python
FROM python:3.10-slim AS builder

WORKDIR /app

# Instala dependências de sistema necessárias para compilar alguns pacotes Python
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python, otimizando o cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Estágio 2: Runtime - Imagem final, menor e mais segura
FROM python:3.10-slim AS runtime

WORKDIR /app

# Cria um usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash nonroot

# Copia as dependências Python instaladas do estágio builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copia o código da aplicação
COPY src/ ./src/

USER nonroot
EXPOSE 8088
CMD ["python", "src/main.py"]