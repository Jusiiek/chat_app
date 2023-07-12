from tests.test_main import app_client


JWT_ENDPOINTS = {
	'login_endpoint': '/api/jwt/login/',
	'register_endpoint': '/api/jwt/register/'
}

class TestJWT:
	user_data = {
		"email": "test@test.com",
		"username": "test_from_test",
		"password": "12zaqWSX!@",
		"re_password": "12zaqWSX!@"
	}

	def test_register(self):
		res = app_client.post(
			JWT_ENDPOINTS['register_endpoint'],
			data=self.user_data
		)

		assert res.status_code == 200

	def test_login(self):
		res = app_client.post(
			JWT_ENDPOINTS['login_endpoint'],
			data={
				"username": self.user_data['username'],
				"password": self.user_data['password']
			}
		)

		assert res.status_code == 200
