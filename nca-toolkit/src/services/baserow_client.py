import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

class BaserowClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def log_entry(self, table_id, data):
        url = f"{self.base_url}/api/database/rows/table/{table_id}/"
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()


# --- Exemplo de rota Flask (fora da classe) ---
@app.route('/insight', methods=['POST'])
def insight():
    content = request.get_json()

    # exemplo de entrada JSON
    data = {
        "input": f"""
        Aja como um roteirista e teólogo especializado em narrativas digitais para redes sociais...
        Título: {content.get('titulo')}
        Descrição: {content.get('descricao')}
        Mensagem Central: {content.get('mensagem')}
        """
    }

    baserow = BaserowClient(base_url="https://api.baserow.io", api_key="SEU_TOKEN_AQUI")
    response = baserow.log_entry(table_id=12345, data=data)

    return jsonify(response)
