def test_list(app_auth_client, endpoint):
	res = app_auth_client.get(endpoint)
	assert res.status_code == 200
	data = res.json()
	assert data and isinstance(data, list)
	return data



def test_get(app_auth_client, endpoint, id):
	res = app_auth_client.get(f'{endpoint}{id}/')
	assert res.status_code == 200
	data = res.json()
	assert data and isinstance(data, dict) and data['user_id']
	return data


def test_create(app_auth_client, endpoint, data):
	res = app_auth_client.post(
		endpoint,
		json=data
	)

	assert res.status_code == 200
	data = res.json()
	assert data and isinstance(data, dict) and data['user_id']
	return data


def test_update(app_auth_client, endpoint, id, data):
	res = app_auth_client.put(
		f"{endpoint}{id}/",
		json=data
	)

	assert res.status_code == 200
	data = res.json()
	assert data and isinstance(data, dict) and data['user_id']
	return data


def test_delete(app_auth_client, endpoint, id):
	res = app_auth_client.delete(
		f"{endpoint}{id}/"
	)

	assert res.status_code == 200
