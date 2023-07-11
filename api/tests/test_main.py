import pytest
from fastapi.testclient import TestClient

from app import register_routes, app

register_routes()
app_client = TestClient(app)


@pytest.fixture
def client():
	user_data = {
		"username": "great_admin",
		"password": "T3stC00mon"
	}
	res = app_client.post(
		'/api/jwt/login/',
		data=user_data
	)
	data = res.json()
	app_client.headers.update(
		{"Authorization": f"{data['token_type']} {data['token']}"}
	)

	return client