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
import urllib
import json

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

template = "http://ip-api.com/json/"

def data_fromip(ip) :
	url = template + ip
	page = urllib.urlopen(url)
	# getting json
	stringjson = page.read()
	datajson = json.loads(stringjson)
	return datajson

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
        self.render("form.html")

    def post(self) :
    	ip = self.request.get("ip")
    	data = data_fromip(ip)
    	country = data["country"]
    	region = data["region"]
    	city = data["city"]
    	self.render("form.html", country = country, region = region, city = city)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
