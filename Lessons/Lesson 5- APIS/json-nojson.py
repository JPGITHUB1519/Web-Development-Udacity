import json

# json

# converting to json
fjson = json.loads('{"one" : 1, "two" : 2}')
print fjson["one"]

# converting to string again
nojson = json.dumps(fjson)

print nojson[3]