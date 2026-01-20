import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    """TestClientのfixtureを提供し、テスト間での再利用を可能にする"""
    return TestClient(app)
