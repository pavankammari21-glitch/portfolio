def test_health_check(client):
    response = client.get("/api/analytics/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "FastAPI" in response.headers.get("X-Powered-By", "")
    assert "X-Process-Time-Sec" in response.headers

def test_overview_endpoint(client):
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["developer"]["name"] == "Pavan"
    assert data["data"]["stats"]["total_projects"] > 0
