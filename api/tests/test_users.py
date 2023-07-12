from tests.test_main import app_client

from utils.test_utils import test_list

USERS_ENDPOINTS = {
	"users": "api/users/",
}


class TestUsers:
	user_data = {
		"email": "test_users@test.com",
		"username": "test_create_users",
		"password": "12zaqWSX!@",
		"re_password": "12zaqWSX!@"
	}

	def test_get_list_of_users(self):
		test_list(
			app_client,
			USERS_ENDPOINTS['users']
		)
