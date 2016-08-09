# User Instructions
# 
# Write a function 'sub1' that, given a 
# string, embeds that string in 
# the string: 
# "I think X is a perfectly normal thing to do in public."
# where X is replaced by the given 
# string.
# The function should return the new string.

given_string = "I think %s is a perfectly normal thing to do in public."

def sub1(s):
	global given_string
	given_string = given_string.replace("%s", s)

	return given_string


print sub1("running") 
# => "I think running is a perfectly normal thing to do in public."    
print sub1("sleeping") 
# => "I think sleeping is a perfectly normal thing to do in public."
