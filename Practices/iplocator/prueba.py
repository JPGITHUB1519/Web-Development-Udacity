import urllib
import json

template = "http://ip-api.com/json/"

def data_fromip(ip) :
	url = template + ip
	page = urllib.urlopen(url)
	# getting json
	stringjson = page.read()
	datajson = json.loads(stringjson)
	return datajson

data = data_fromip("179.52.116.37")

print data["country"]