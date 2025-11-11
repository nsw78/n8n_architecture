#!/bin/bash
# --------------------------------------------------------------------
# Script de backup dos volumes Docker do ambiente "ambiente-nca"
# Autor: Nelson dos Santos Walcow
# --------------------------------------------------------------------

# Diretório onde os backups serão salvos
BACKUP_DIR="$(pwd)/backup"
mkdir -p "$BACKUP_DIR"

# Data atual
DATE=$(date +%F)

# Lista de volumes relevantes (ajuste conforme seus volumes reais)
VOLUMES=(
  "ambiente-nca_postgres_data"
  "ambiente-nca_minio_data"
  "ambiente-nca_n8n_data"
  "ambiente-nca_baserow_data"
  "ambiente-nca_ollama_data"
  "ambiente-nca_kokoro_data"
)

echo "============================================================"
echo "🚀 Iniciando backup dos volumes Docker do ambiente NCA"
echo "📦 Diretório de backup: $BACKUP_DIR"
echo "📅 Data: $DATE"
echo "============================================================"
echo ""

# Loop pelos volumes
for VOLUME in "${VOLUMES[@]}"; do
  echo "🔹 Verificando volume: $VOLUME"
  if docker volume inspect "$VOLUME" &>/dev/null; then
    BACKUP_FILE="${BACKUP_DIR}/${VOLUME}_${DATE}.tar.gz"
    echo "   → Fazendo backup para: $BACKUP_FILE"
    docker run --rm -v ${VOLUME}:/data -v ${BACKUP_DIR}:/backup alpine \
      tar czf /backup/${VOLUME}_${DATE}.tar.gz /data
    echo "   ✅ Backup concluído."
  else
    echo "   ⚠️ Volume não encontrado: $VOLUME (ignorando)"
  fi
  echo ""
done

echo "============================================================"
echo "✅ Todos os backups concluídos!"
echo "📁 Arquivos salvos em: $BACKUP_DIR"
echo "============================================================"
