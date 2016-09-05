import time

# complex_computation() simulates a slow function. time.sleep(n) causes the
# program to pause for n seconds. In real life, this might be a call to a
# database, or a request to another web service.
def complex_computation(a, b):
    time.sleep(.5)
    return a + b

# QUIZ - Improve the cached_computation() function below so that it caches
# results after computing them for the first time so future calls are faster
cache = {}
def cached_computation(a, b):
	key = make_key(a,b)

	if key in cache :
		r = cache[key]
	else :
		r = complex_computation(a,b)
		cache[key] = r
	return r

def make_key(a,b) :
	key = "%s,%s" % (a,b)
	return key

start_time = time.time()
print cached_computation(5, 4)
print "the first computation took %f seconds" % (time.time() - start_time)

start_time2 = time.time()
print cached_computation(5, 4)
print "the second computation took %f seconds" % (time.time() - start_time2)

