from tests.test_main import app_client


JWT_ENDPOINTS = {
	'login_endpoint': '/api/jwt/login/',
	'register_endpoint': '/api/jwt/register/'
}

class TestJWT:
	def test_login(self):
		user_data = {
			"username": "great_admin",
			"password": "T3stC00mon"
		}

		res = app_client.post(
			JWT_ENDPOINTS['login_endpoint'],
			data=user_data
		)

		assert res.status_code == 200


	def test_register(self):
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

		assert res.status_code == 200
