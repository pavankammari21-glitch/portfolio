from app.config import settings

def test_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_info"]["username"] == settings.ADMIN_USERNAME

def test_login_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={"username": settings.ADMIN_USERNAME, "password": "wrongpassword123"}
    )
    assert response.status_code == 401
    assert response.json()["success"] is False

def test_oauth2_token_endpoint(client):
    response = client.post(
        "/api/auth/token",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_protected_me_endpoint_with_valid_token(client):
    login_res = client.post(
        "/api/auth/login",
        json={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD}
    )
    token = login_res.json()["access_token"]
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == settings.ADMIN_USERNAME

def test_protected_me_endpoint_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
