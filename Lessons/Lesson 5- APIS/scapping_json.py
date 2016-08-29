import json

# \\ for scapping
j = json.loads('{"name" : "je\\"an"}')

print j["name"]