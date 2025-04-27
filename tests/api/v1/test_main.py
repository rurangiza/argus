from fastapi.testclient import TestClient


def test_health(client: TestClient):
	response = client.get('/health')
	assert response.json() == {'health': 'ok'}

def test_readiness(client: TestClient):
	response = client.get('/ready')
	assert response.json() == {'status': 'ready'}
