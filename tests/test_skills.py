from app.config import settings

def test_list_skills(client):
    response = client.get('/api/skills')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) > 0

def test_list_skills_filter_category(client):
    response = client.get('/api/skills?category=Backend')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for s in data['data']:
        assert 'Backend' in s['category']

def test_list_categorized_skills(client):
    response = client.get('/api/skills/categorized')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    categories = [cat['category'] for cat in data['data']]
    assert any('Backend' in cat for cat in categories)

def test_resume_json(client):
    response = client.get('/api/resume/json')
    assert response.status_code == 200
    data = response.json()
    assert 'basics' in data
    assert 'Pavan' in data['basics']['name']

def test_resume_download_html(client):
    response = client.get('/api/resume/download')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Pavan' in response.text
    assert 'last_resume_download' in response.headers.get('set-cookie', '')

def test_create_skill_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    payload = {
        'name': 'GraphQL & Strawberry',
        'category': 'Backend',
        'proficiency': 88,
        'experience_years': '2+ years',
        'icon': '🍓',
        'is_primary': True
    }
    response = client.post(
        '/api/skills',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    data = response.json()
    assert data['success'] is True
    assert data['data']['name'] == payload['name']

def test_create_skill_duplicate_conflict(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    payload = {
        'name': 'FastAPI',
        'category': 'Backend',
        'proficiency': 99
    }
    response = client.post(
        '/api/skills',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 409

def test_create_skill_unauthorized(client):
    response = client.post(
        '/api/skills',
        json={'name': 'Unauthorized Skill', 'category': 'Testing', 'proficiency': 50}
    )
    assert response.status_code == 401
