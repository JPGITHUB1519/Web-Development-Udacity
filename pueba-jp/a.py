import re

user_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

print user_check.match("Je")