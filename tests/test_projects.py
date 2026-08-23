from app.config import settings
import io

def test_list_projects(client):
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['items']) > 0
    assert 'meta' in data

def test_filter_projects_by_tech(client):
    response = client.get('/api/projects?tech=FastAPI')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) > 0
    for item in data['items']:
        assert any('fastapi' in t.lower() for t in item['tech_stack'])

def test_search_projects(client):
    response = client.get('/api/projects?search=microservices')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['items']) >= 1

def test_get_project_by_id(client):
    list_res = client.get('/api/projects')
    first_id = list_res.json()['items'][0]['id']

    response = client.get(f'/api/projects/{first_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == first_id

def test_get_nonexistent_project(client):
    response = client.get('/api/projects/999999')
    assert response.status_code == 404
    assert response.json()['success'] is False

def test_create_project_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    new_project_payload = {
        'title': 'Automated Testing Pipeline API',
        'summary': 'Continuous integration test execution runner built with FastAPI.',
        'description': 'Comprehensive test execution backend running automated pytest assertions in parallel workers.',
        'tech_stack': ['FastAPI', 'Pytest', 'Docker', 'Python'],
        'category': 'DevOps',
        'is_featured': True,
        'stars_count': 15
    }

    response = client.post(
        '/api/projects',
        json=new_project_payload,
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    data = response.json()
    assert data['data']['title'] == new_project_payload['title']

def test_create_project_unauthorized(client):
    response = client.post(
        '/api/projects',
        json={'title': 'Unauthorized Project', 'summary': 'Short', 'description': 'Invalid', 'tech_stack': ['Python']}
    )
    assert response.status_code == 401

def test_update_project_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    list_res = client.get('/api/projects')
    first_id = list_res.json()['items'][0]['id']

    update_res = client.put(
        f'/api/projects/{first_id}',
        json={'stars_count': 999},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert update_res.status_code == 200
    assert update_res.json()['success'] is True
    assert update_res.json()['data']['stars_count'] == 999

def test_update_project_unauthorized(client):
    response = client.put('/api/projects/1', json={'stars_count': 500})
    assert response.status_code == 401

def test_upload_thumbnail_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    list_res = client.get('/api/projects')
    first_id = list_res.json()['items'][0]['id']

    fake_image = io.BytesIO(b'fake png content data')
    files = {'file': ('test_image.png', fake_image, 'image/png')}

    resp = client.post(
        f'/api/projects/{first_id}/thumbnail',
        files=files,
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 200
    assert resp.json()['success'] is True
    assert 'image_url' in resp.json()['data']

def test_upload_thumbnail_unsupported_type(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    list_res = client.get('/api/projects')
    first_id = list_res.json()['items'][0]['id']

    fake_file = io.BytesIO(b'some binary content')
    files = {'file': ('test.exe', fake_file, 'application/x-msdownload')}

    resp = client.post(
        f'/api/projects/{first_id}/thumbnail',
        files=files,
        headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == 415

def test_delete_project_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    create_res = client.post(
        '/api/projects',
        json={
            'title': 'Temp Project To Delete',
            'summary': 'Temporary project created for automated deletion verification.',
            'description': 'Comprehensive description for the temporary project created for testing deletion.',
            'tech_stack': ['FastAPI', 'Python']
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    project_id = create_res.json()['data']['id']

    delete_res = client.delete(
        f'/api/projects/{project_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert delete_res.status_code == 200
    assert delete_res.json()['success'] is True

def test_delete_project_unauthorized(client):
    response = client.delete('/api/projects/1')
    assert response.status_code == 401
