import json


def get_auth_token(client, username, password):
    response = client.post('/api/login', data=json.dumps({
        'username': username,
        'password': password
    }), content_type='application/json')
    assert response.status_code == 200, f"Login failed with status {response.status_code}: {response.get_data(as_text=True)}"
    return json.loads(response.data)['access_token']


def test_login_user(client, setup_database):
    user, _ = setup_database

    response = client.post('/api/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

    assert response.status_code == 200, f"Response status code was {response.status_code} with data {response.get_data(as_text=True)}"
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['username'] == 'testuser'


def test_prisoner_statistics_without_auth(client, init_database):
    response = client.get('/api/statistics')
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data


def test_prisoner_statistics_with_auth(client, setup_database):
    user, _ = setup_database
    token = get_auth_token(client, user.username, 'testpassword')

    response = client.get('/api/statistics', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'crime_count' in data
    assert 'average_sentence_by_crime' in data
    assert 'gender_distribution' in data


def test_get_prisoner(client, setup_database):
    user, prisoner = setup_database
    token = get_auth_token(client, user.username, 'testpassword')

    response = client.get(f'/api/prisoners/{prisoner.prisoner_id}', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'
    assert data['age'] == 30


def test_get_non_existing_prisoner(client, setup_database):
    user, _ = setup_database
    token = get_auth_token(client, user.username, 'testpassword')

    response = client.get('/api/prisoners/999', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Prisoner not found'





