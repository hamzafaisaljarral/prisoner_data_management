import json


def get_auth_token(client, username, password):
    response = client.post('/api/login', data=json.dumps({
        'username': username,
        'password': password
    }), content_type='application/json')

    # Add debug information
    print(f"Login response data: {response.get_data(as_text=True)}")

    assert response.status_code == 200, f"Login failed with status {response.status_code}"
    data = json.loads(response.data)
    assert 'access_token' in data, f"access_token is missing in response data: {data}"
    return data['access_token']


def test_register_user(client, init_database):
    response = client.post('/api/register', data=json.dumps({
        'username': 'newuser',
        'password': 'newpassword'
    }), content_type='application/json')

    assert response.status_code == 201
    assert b'User registered successfully' in response.data


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


def test_prisoner_statistics_without_auth(client):
    response = client.get('/api/statistics')
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data


def test_prisoner_statistics_with_auth(client, setup_database):
    user, _ = setup_database

    response = client.post('/api/login', data=json.dumps({
        'username': user.username,
        'password': 'testpassword'
    }), content_type='application/json')

    assert response.status_code == 200, f"Login failed with status {response.status_code}"
    data = json.loads(response.data)
    assert 'access_token' in data, f"access_token is missing in response data: {data}"
    access_token = data['access_token']

    response = client.get('/api/statistics', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'crime_count' in data
    assert 'average_sentence_by_crime' in data
    assert 'gender_distribution' in data


def test_age_distribution_without_auth(client):
    response = client.get('/api/age-distribution')
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data


def test_age_distribution_with_auth(client, setup_database):
    user, _ = setup_database
    token = get_auth_token(client, user.username, 'testpassword')

    response = client.get('/api/age-distribution', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list), "Expected data to be a list"
    if data:  # if there's any data
        assert 'age' in data[0], "Each record should have 'age' column"
        assert 'count' in data[0], "Each record should have 'count' column"


def test_prison_population_without_auth(client):
    response = client.get('/api/prison-population')
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data


def test_prison_population_with_auth(client, setup_database):
    user, _ = setup_database
    token = get_auth_token(client, user.username, 'testpassword')

    response = client.get('/api/prison-population', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list), "Expected data to be a list"
    if data:  # if there's any data
        assert 'prison_name' in data[0], "Each record should have 'prison_name' column"
        assert 'count' in data[0], "Each record should have 'count' column"