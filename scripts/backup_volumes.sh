#!/bin/sh
# =====================================================================
# 🔄 Script de backup automático para volumes Docker
# =====================================================================

set -e

while true; do
  echo "[$(date)] Executando backup dos volumes..."
  
  # Garante que o diretório de backup exista
  mkdir -p /backup
  
  tar czf "/backup/postgres_backup_$(date +%F_%H-%M-%S).tar.gz" -C /data_postgres .
  tar czf "/backup/minio_backup_$(date +%F_%H-%M-%S).tar.gz" -C /data_minio .
  tar czf "/backup/baserow_backup_$(date +%F_%H-%M-%S).tar.gz" -C /data_baserow .
  
  echo "[$(date)] Backup concluído. Próxima execução em 24 horas."
  sleep 86400
done