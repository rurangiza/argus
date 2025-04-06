from fastapi.testclient import TestClient


def test_chat(client: TestClient):
	response = client.get('/chat')
	assert response.json() == {'message': 'How may I help you?'}
