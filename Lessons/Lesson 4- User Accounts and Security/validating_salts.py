import random
import string
import hashlib

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def generate_hash(name, pw, salt) :
	return hashlib.sha256(name + pw + salt).hexdigest()

def make_pw_hash(name, pw):
    salt = make_salt()
    h = generate_hash(name, pw, salt)
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    ###Your code here

    obtain_salt = h.split(',')[1]
    test_h = generate_hash(name, pw, obtain_salt) + "," + obtain_salt
    if  test_h == h :
    	return True
    return False

h = make_pw_hash('spez', 'hunter2')
print valid_pw('spez', 'hunter2', h)

