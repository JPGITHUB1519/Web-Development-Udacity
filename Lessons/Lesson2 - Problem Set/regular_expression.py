import re

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username) :

	return user_re.match(username)


