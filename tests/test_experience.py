from app.config import settings

def test_list_experience(client):
    response = client.get("/api/experience")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["result"] if "result" in data else data["data"]) > 0

def test_filter_experience_by_type(client):
    response = client.get("/api/experience?item_type=work")
    assert response.status_code == 200
    data = response.json()
    items = data["data"]
    for item in items:
        assert item["item_type"] == "work"

def test_create_experience_authenticated(client):
    login_res = client.post(
        "/api/auth/login",
        json={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD}
    )
    token = login_res.json()["access_token"]

    payload = {
        "role_or_degree": "Principal Backend Architect",
        "organization": "Global Cloud Systems",
        "period": "2024 - Present",
        "location": "Hyderabad, India",
        "item_type": "work",
        "description": "Designing large-scale distributed asynchronous backend infrastructure.",
        "key_achievements": ["Scaled FAstAPI cluster to 100K+ RPS", "Built event-driven messaging pipelines"],
        "skills_used": ["FastAPI", "Python", "Kafka", "Docker"],
        "order_index": 0
    }

    response = client.post(
        "/api/experience",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["role_or_degree"] == payload["role_or_degree"]

def test_create_experience_unauthorized(client):
    response = client.post(
        "/api/experience",
        json={"role_or_degree": "Unauthorized Role", "organization": "XYZ", "period": "2026"}
    )
    assert response.status_code == 401
