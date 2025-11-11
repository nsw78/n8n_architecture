#!/bin/bash
# --------------------------------------------------------------------
# Script de restauração dos volumes Docker do ambiente "ambiente-nca"
# Autor: Nelson Walcow
# --------------------------------------------------------------------

# Diretório onde os backups estão armazenados
BACKUP_DIR="$(pwd)/backup"

# Verifica se o diretório existe
if [ ! -d "$BACKUP_DIR" ]; then
  echo "❌ Diretório de backup não encontrado: $BACKUP_DIR"
  echo "Crie o diretório ou execute primeiro o script de backup."
  exit 1
fi

# Lista todos os arquivos de backup disponíveis
echo "============================================================"
echo "🧱 Backups disponíveis no diretório: $BACKUP_DIR"
echo "============================================================"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null || echo "Nenhum arquivo de backup encontrado."
echo "============================================================"
echo ""

# Solicita o nome do arquivo de backup a restaurar
read -p "Digite o nome exato do arquivo de backup (.tar.gz) que deseja restaurar: " BACKUP_FILE

# Caminho completo
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Verifica se o arquivo existe
if [ ! -f "$BACKUP_PATH" ]; then
  echo "❌ Arquivo de backup não encontrado: $BACKUP_PATH"
  exit 1
fi

# Extrai o nome do volume a partir do arquivo
VOLUME_NAME=$(echo "$BACKUP_FILE" | cut -d'_' -f1-4)

# Confirmação do usuário
echo ""
echo "============================================================"
echo "🚨 Você está prestes a restaurar o volume: $VOLUME_NAME"
echo "📦 Arquivo de origem: $BACKUP_FILE"
echo "⚠️ Isso substituirá todos os dados atuais do volume."
echo "============================================================"
read -p "Deseja continuar? (digite 'SIM' para confirmar): " CONFIRM

if [ "$CONFIRM" != "SIM" ]; then
  echo "❌ Operação cancelada pelo usuário."
  exit 0
fi

# Verifica se o volume existe, caso contrário, cria
if ! docker volume inspect "$VOLUME_NAME" &>/dev/null; then
  echo "🔹 Volume não encontrado. Criando: $VOLUME_NAME"
  docker volume create "$VOLUME_NAME" >/dev/null
fi

# Executa a restauração
echo "🔁 Restaurando dados para o volume $VOLUME_NAME..."
docker run --rm -v "${VOLUME_NAME}:/data" -v "${BACKUP_DIR}:/backup" alpine \
  sh -c "rm -rf /data/* && tar xzf /backup/${BACKUP_FILE} -C /"

echo "✅ Restauração concluída com sucesso."
echo "============================================================"
echo "Volume restaurado: $VOLUME_NAME"
echo "Origem: $BACKUP_FILE"
echo "Data: $(date)"
echo "============================================================"
