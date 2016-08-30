import json
import urllib2


def wheather_data(city_name):
	url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=d20c9a278fe26aa2d12bc4fa3cfda66e" % city_name
	# making request
	page = urllib2.urlopen(url)
	result= {}
	data_json = page.read()
	json_decode = json.loads(data_json)
	# main
	result["weather"] = json_decode["weather"][0]["main"]
	# description
	result["description"] = json_decode["weather"][0]["description"]
	# temperature
	result["temp"] = json_decode["main"]["temp"]

	return result

print wheather_data("Santiago")