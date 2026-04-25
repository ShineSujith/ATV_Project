from fastapi.testclient import TestClient
from src.app.microphone_service import app, stop_event
from unittest.mock import AsyncMock, patch
import pytest

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_rabbitmq():
    with patch('src.app.microphone_service.get_exchange') as mock_get_exchange:
        mock_conn = AsyncMock()
        mock_ch = AsyncMock()
        mock_ex = AsyncMock()
        mock_get_exchange.return_value = (mock_conn, mock_ch, mock_ex)
        yield mock_get_exchange
