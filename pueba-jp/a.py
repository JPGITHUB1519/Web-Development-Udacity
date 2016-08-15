import hashlib
import hmacj
a = hashlib.md5("1").hexdigest()
print a

print hmacj.new("python", "100").hexdigest()