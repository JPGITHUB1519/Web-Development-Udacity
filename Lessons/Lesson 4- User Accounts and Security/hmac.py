import hashlib
import hmac

encripted = hashlib.md5("udacity").hexdigest()

encripted = hmac.new("secret", "udacity").hexdigest()



print hmac.new("secret", "udacity")