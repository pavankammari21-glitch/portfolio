def test_middleware_headers_injected(client):
    response = client.get('/api/analytics/health')
    assert response.status_code == 200
    assert 'x-process-time-sec' in response.headers
    assert 'x-powered-by' in response.headers
    assert response.headers['x-powered-by'] == 'FastAPI & Python 3.11'

def test_custom_404_error_structure(client):
    response = client.get('/api/projects/888888')
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert 'error' in data
    assert data['error']['code'] == 'RESOURCE_NOT_FOUND'
    assert 'path' in data['error']

def test_custom_422_validation_error_structure(client):
    response = client.post('/api/contact', json={'name': ''})
    assert response.status_code == 422
    data = response.json()
    assert data['success'] is False
    assert data['error']['code'] == 'VALIDATION_ERROR'
    assert isinstance(data['error']['details'], list)

def test_custom_401_error_structure(client):
    response = client.get('/api/auth/me')
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['error']['code'] == 'UNAUTHORIZED'
