import pytest
from fastapi.testclient import TestClient

from src.argus.main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
