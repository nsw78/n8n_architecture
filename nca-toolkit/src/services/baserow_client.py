class BaserowClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def log_entry(self, table_id, data):
        import requests

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