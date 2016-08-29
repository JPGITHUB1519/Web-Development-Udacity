import json

# json has to always have doble quote for name properties
x = json.loads('{"blah":["one", 2, "th\\"r\\"ee"]}')

print x