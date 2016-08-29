import json

jstring = '{"one" : 1, "numbers" : [1,2,3,4,5]}'

# decodificar un JSON
jjson = json.loads(jstring)


print jjson["one"]

for i in jjson :

	print jjson[i]
