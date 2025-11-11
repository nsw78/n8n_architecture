#!/usr/bin/env bash
# =====================================================================
# 🚀 Script de inicialização do ambiente NCA (Nelson Cloud Automation)
# Autor: Nelson dos Santos Walcow
# Data: $(date +%d/%m/%Y)
# =====================================================================

set -e  # Para o script se houver erro
PROJECT_NAME="ambiente-nca"

echo "=============================================================="
echo "🔧 Iniciando setup do ambiente NCA..."
echo "=============================================================="
sleep 1

# ------------------------------------------------------------
# 1️⃣ Verificar dependências básicas
# ------------------------------------------------------------
echo "🔍 Verificando dependências..."
for cmd in docker docker compose curl; do
  if ! command -v $cmd &> /dev/null; then
    echo "❌ Dependência faltando: $cmd"
    echo "   ➤ Instale antes de continuar."
    exit 1
  fi
done
echo "✅ Dependências OK!"
sleep 1

# ------------------------------------------------------------
# 2️⃣ Criar pastas e volumes
# ------------------------------------------------------------
echo "📂 Criando diretórios necessários..."
mkdir -p data kokoro nca-toolkit logs
mkdir -p kokoro/models nca-toolkit/src
echo "✅ Estrutura de diretórios criada."
sleep 1

# ------------------------------------------------------------
# 3️⃣ Parar containers antigos (se existirem)
# ------------------------------------------------------------
echo "🧹 Limpando containers antigos..."
docker compose down -v --remove-orphans || true
echo "✅ Containers antigos removidos."
sleep 1

# ------------------------------------------------------------
# 4️⃣ Construir imagens personalizadas
# ------------------------------------------------------------
echo "🏗️ Construindo imagens (Kokoro + NCA Toolkit)..."
docker compose build kokoro nca-toolkit
echo "✅ Build concluído."
sleep 1

# ------------------------------------------------------------
# 5️⃣ Subir todos os containers
# ------------------------------------------------------------
echo "🚀 Subindo stack principal (${PROJECT_NAME})..."
docker compose up -d
sleep 3

# ------------------------------------------------------------
# 6️⃣ Verificar status dos containers
# ------------------------------------------------------------
echo "🔎 Verificando status de saúde..."
sleep 5
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# ------------------------------------------------------------
# 7️⃣ Healthcheck geral (aguarda até 3 minutos)
# ------------------------------------------------------------
echo ""
echo "⏳ Aguardando containers ficarem saudáveis (até 3 minutos)..."
TIMEOUT=180
INTERVAL=10
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
  UNHEALTHY=$(docker ps --filter "health=unhealthy" --format "{{.Names}}")
  if [ -z "$UNHEALTHY" ]; then
    echo "✅ Todos os containers estão saudáveis!"
    break
  fi
  echo "⌛ Ainda aguardando: $UNHEALTHY"
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

if [ $ELAPSED -ge $TIMEOUT ]; then
  echo "⚠️ Alguns containers não ficaram saudáveis a tempo."
  docker ps --filter "health=unhealthy"
else
  echo "🎯 Ambiente NCA pronto para uso!"
fi

# ------------------------------------------------------------
# 8️⃣ Exibir URLs de acesso
# ------------------------------------------------------------
echo ""
echo "=============================================================="
echo "🌐 URLs do ambiente NCA"
echo "=============================================================="
echo "🔗 n8n:            http://localhost:5680"
echo "🔗 Baserow:        http://localhost:8081"
echo "🔗 MinIO Console:  http://localhost:9006"
echo "🔗 Kokoro TTS:     http://localhost:5002"
echo "🔗 NCA Toolkit:    http://localhost:8088"
echo "🔗 Ollama API:     http://localhost:11434"
echo "=============================================================="
echo "💾 Logs: salvos em ./logs/"
echo "=============================================================="
