def test_websocket_live_stats(client):
    with client.websocket_connect("/ws/live-stats") as websocket:
        # 1. Receive visitor count broadcast upon connecting
        data = websocket.receive_json()
        assert data["type"] == "visitor_count"
        assert data["active_visitors"] >= 1

        # 2. Send ping command
        websocket.send_json({"command": "ping"})
        response = websocket.receive_json()
        assert response["type"] == "pong"
        assert "timestamp" in response

        # 3. Send server_info command
        websocket.send_json({"command": "server_info"})
        info_res = websocket.receive_json()
        assert info_res["type"] == "server_info"
        assert "platform" in info_res
