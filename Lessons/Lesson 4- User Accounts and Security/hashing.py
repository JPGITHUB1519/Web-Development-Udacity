import hashlib



encripted = hashlib.md5("hello")

#encripted = hashlib.sha1("hello")
print encripted.hexdigest()