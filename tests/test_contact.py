from app.config import settings

def test_contact_form_submission_success(client):
    payload = {
        'name': 'Alex Johnson',
        'email': 'alex@enterprise-cloud.io',
        'subject': 'FastAPI Lead Role',
        'message': 'We are hiring for a Senior FastAPI Backend Engineer role.'
    }
    response = client.post('/api/contact', json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data['success'] is True
    assert 'inquiry_id' in data
    assert 'Alex Johnson' in data['message']

def test_contact_form_validation_failure(client):
    payload = {
        'name': 'A',
        'email': 'invalid-email-address',
        'message': 'Hi'
    }
    response = client.post('/api/contact', json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data['success'] is False
    assert data['error']['code'] == 'VALIDATION_ERROR'

def test_list_inbox_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    response = client.get(
        '/api/contact/inbox',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)

def test_list_inbox_unauthorized(client):
    response = client.get('/api/contact/inbox')
    assert response.status_code == 401

def test_mark_message_as_read_authenticated(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    # Submit a message
    submit_res = client.post(
        '/api/contact',
        json={'name': 'Tester', 'email': 'tester@example.com', 'subject': 'Test', 'message': 'Message to read'}
    )
    inquiry_id = submit_res.json()['inquiry_id']

    patch_res = client.patch(
        f'/api/contact/inbox/{inquiry_id}/read',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()['data']['is_read'] is True

def test_mark_nonexistent_message_as_read(client):
    login_res = client.post(
        '/api/auth/login',
        json={'username': settings.ADMIN_USERNAME, 'password': settings.ADMIN_PASSWORD}
    )
    token = login_res.json()['access_token']

    patch_res = client.patch(
        '/api/contact/inbox/999999/read',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert patch_res.status_code == 404
