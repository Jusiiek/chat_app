import pytest
from fastapi.testclient import TestClient

from app import register_routes, app

register_routes()
app_client = TestClient(app)


JWT_ENDPOINTS = {
	'login_endpoint': '/api/jwt/login/',
	'register_endpoint': '/api/jwt/register/'
}

#TODO register and login still not working
def login_test():
	user_data = {
		"username": "great_admin",
		"password": "T3stC00mon"
	}

	res = app_client.post(
		JWT_ENDPOINTS['login_endpoint'],
		data=user_data
	)

	print(res)
	assert res.status_code == 200


def register_test():
	user_data = {
		"email": "test@test.com",
		"username": "test_from_test",
		"password": "12zaqWSX!@",
		"re_password": "12zaqWSX!@"
	}

	res = app_client.post(
		JWT_ENDPOINTS['register_endpoint'],
		data=user_data
	)

	print(res)
	assert res.status_code == 200
	data = res.json()
