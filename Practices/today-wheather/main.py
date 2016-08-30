#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import json
import urllib2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

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

class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("index.html")

    def post(self) :
    	city = self.request.get("city")
    	data = wheather_data(city)
    	wheather = data["weather"]
    	description = data["description"]
    	temperature = data["temp"]
    	self.render("index.html", wheather = wheather, description = description, temperature = temperature)
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
