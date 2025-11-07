import pytest
from src.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_insight(client):
    response = client.post('/insight', json={"input": "test"})
    assert response.status_code == 200
    assert "response" in response.json

def test_upload(client):
    data = {
        'file': (io.BytesIO(b'test file content'), 'test.txt')
    }
    response = client.post('/upload', data=data)
    assert response.status_code == 200
    assert response.json == {"message": "File uploaded successfully"}

def test_log(client):
    response = client.post('/log', json={"entry": "test log entry"})
    assert response.status_code == 200
    assert response.json == {"message": "Log entry created successfully"}