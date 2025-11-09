import requests
import json

# ========================
# CONFIGURAÇÕES DO BASEROW
# ========================
BASEROW_URL = "http://localhost:8081/api"
API_TOKEN = "SEU_TOKEN_AQUI"  # <-- Substitua pelo seu token real
HEADERS = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}

# ========================
# 1️⃣ CRIAR DATABASE
# ========================
db_data = {"name": "DarkSiteProfetico"}
resp = requests.post(f"{BASEROW_URL}/applications/", headers=HEADERS, data=json.dumps(db_data))
if resp.status_code not in (200, 201):
    print("❌ Erro ao criar database:", resp.text)
    exit()
database_id = resp.json()["id"]
print(f"✅ Database criado: ID = {database_id}")

# ========================
# 2️⃣ CRIAR TABELA MensagensProfeticas
# ========================
table_data = {"name": "MensagensProfeticas", "database_id": database_id}
resp = requests.post(f"{BASEROW_URL}/database/tables/", headers=HEADERS, data=json.dumps(table_data))
if resp.status_code not in (200, 201):
    print("❌ Erro ao criar tabela:", resp.text)
    exit()
table_id = resp.json()["id"]
print(f"✅ Tabela criada: ID = {table_id}")

# ========================
# 3️⃣ CRIAR CAMPOS
# ========================
fields = [
    {"name": "Título", "type": "text"},
    {"name": "Descrição", "type": "long_text"},
    {"name": "Data", "type": "date"},
    {"name": "Status", "type": "single_select", "select_options": [
        {"value": "Publicado", "color": "green"},
        {"value": "Rascunho", "color": "yellow"},
    ]},
    {"name": "Link_S3", "type": "url"},
]

for field in fields:
    resp = requests.post(f"{BASEROW_URL}/database/fields/table/{table_id}/", headers=HEADERS, data=json.dumps(field))
    if resp.status_code not in (200, 201):
        print(f"❌ Erro ao criar campo {field['name']}:", resp.text)
    else:
        print(f"✅ Campo criado: {field['name']}")

print("\n🎉 Tabela 'MensagensProfeticas' criada com sucesso no Baserow!")
print("Você pode acessar via interface web e confirmar os campos.")
