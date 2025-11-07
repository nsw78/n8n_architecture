# Estágio 1: Builder - Instala dependências de sistema e Python
FROM python:3.10-slim AS builder

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python, otimizando o cache
COPY requirements.txt* .
RUN if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    else \
      pip install --no-cache-dir flask; \
    fi

# Estágio 2: Runtime - Imagem final, menor e mais segura
FROM python:3.10-slim AS runtime

WORKDIR /app

# Cria um usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash nonroot

# Copia dependências de sistema e Python do estágio builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/bin/ffmpeg /usr/bin/ffmpeg

# Copia o código da aplicação
COPY . .

# Cria um fallback se o código principal não existir
RUN if [ ! -f app.py ] && [ ! -f main.py ]; then \
      printf "from flask import Flask, jsonify\napp = Flask(__name__)\n@app.route('/')\ndef index():\n    return 'Kokoro placeholder: coloque seu código em /kokoro'\n\n@app.route('/health')\ndef health():\n    return jsonify({'status': 'ok'})\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=5002)\n" > /app/app.py; \
    fi

USER nonroot
EXPOSE 5002
CMD ["sh", "-c", "if [ -f main.py ]; then python main.py; elif [ -f app.py ]; then python app.py; else sleep infinity; fi"]
