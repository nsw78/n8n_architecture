class OllamaClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def generate_response(self, prompt):
        import requests

        response = requests.post(self.api_url, json={"prompt": prompt})
        if response.status_code == 200:
            # Assumindo que a resposta do Ollama tem um campo 'response' ou similar
            return response.json().get("response", response.json())
        else:
            response.raise_for_status()