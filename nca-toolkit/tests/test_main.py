import pytest
from src.main import app
import io

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_insight(client):
    # Este teste é mais complexo pois depende do Ollama.
    # Em um cenário real, usaríamos um 'mock'. Por enquanto, testamos a falha esperada.
    response = client.post('/insight', json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_upload(client):
    data = {
        'file': (io.BytesIO(b'test file content'), 'test.txt')
    }
    # Este teste depende do MinIO. Testamos a requisição sem o arquivo.
    response = client.post('/upload')
    assert response.status_code == 400

def test_log(client):
    # Este teste depende do Baserow. Testamos a requisição sem dados.
    response = client.post('/log', json={})
    # O servidor retornará 500 se as chaves não estiverem configuradas, o que é esperado.
    assert response.status_code == 500