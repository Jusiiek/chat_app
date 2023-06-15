ADMIN_ROLES = ["SUPER_ADMIN", "ADMIN"]


def is_user_super_user(role):
	return role == "SUPER_ADMIN"


def is_user_admin(role):
	return any(role in ADMIN_ROLES)
