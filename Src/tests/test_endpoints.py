from unittest.mock import patch

def test_send_text_input_200(client, mock_rabbitmq):
    result = client.post("/api/sendTextInput", json={"payload": "test"})
    assert result.status_code == 200
    mock_rabbitmq.assert_called()

def test_send_text_input_422(client, mock_rabbitmq):
    result = client.post("/api/sendTextInput")
    assert result.status_code == 422
    mock_rabbitmq.assert_not_called()

def test_start_200(client):
    with patch("src.app.microphone_service.listen_loop"):
        result = client.post("/api/start")
        assert result.status_code == 200
        assert result.json() == {"status": "started"}

def test_start_if_thread_exists(client):
    with patch("src.app.microphone_service.thread") as mock_thread:
        mock_thread.is_alive.return_value = True
        with patch("src.app.microphone_service.threading.Thread") as mock_thread_cls:
            client.post("/api/start")
            mock_thread_cls.assert_not_called()

def test_stop_200(client):
    response = client.post("/api/stop")
    assert response.status_code == 200
    assert response.json() == {"status": "stopped"}
