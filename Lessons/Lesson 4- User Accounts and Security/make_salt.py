import random
import string
from random import randint

abc = map(chr, range(97, 123))
abc += map(chr, range(65, 91))

# implement the function make_salt() that returns a string of 5 random
# letters use python's random module.
# Note: The string package might be useful here.

def make_salt():

	word_list = []
	for cont in range(0,5) :
		rand_number = randint(0,51)
		word_list.append(abc[rand_number])

	return ''.join(word_list)

print make_salt()



