
#handy link
#http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
#maybe a link to itertools

SERVERS = ['SERVER1', 'SERVER2', 'SERVER3', 'SERVER4']

# QUIZ - implement the function get_server, which returns one element from the
# list SERVERS in a round-robin fashion on each call. Note that you should 
# comment out all your 'print get_server()' statements before submitting 
# your code or the grading script may fail. For more info see:
# http://forums.udacity.com/cs253-april2012/questions/22327/unit6-13-quiz-problem-with-submission

n = -1
def get_server():
	global n
	if n == - 1 or n ==  3:
		n = 0
		return SERVERS[0]
	if n == 0 :
		n = 1
		return SERVERS[1]
	if n == 1 :
		n = 2
		return SERVERS[2]
	if n == 2 :
		n = 3
		return SERVERS[3]


    ###Your code here.

print get_server()
print get_server()
print get_server()
print get_server()
print get_server()
print get_server()
print get_server()
print get_server()

# >>> SERVER1
# >>> SERVER2
# >>> SERVER3
# >>> SERVER4
# >>> SERVER1
# >>> SERVER2
# >>> SERVER3
# >>> SERVER4


