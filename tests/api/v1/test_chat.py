from fastapi.testclient import TestClient


def test_incomplete_request(client: TestClient):
    request = {
        'model': 'gpt-4o-mini',
        'temperature': 0.7,
        'top_p': 1.0,
        'stream': False,
        'messages': [
            {'role': 'system', 'content': "You're a helpful assistant"},
            {'role': 'user', 'content': 'why is the sky blue?'},
        ],
        'tools': ['GetDatetime']
    }
    response = client.post('/v1/chat', json=request)
    assert response.status_code == 200
