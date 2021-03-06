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
#
import webapp2
# importing jinja
import jinja2
import os
import psycopg2


# setting the dir of the template = actual pos + templates
template_dir = os.path.join(os.path.dirname(__file__), 'Postgre_and_python_templates')
# setting jinja enviroment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape=True) # autoscape

# helper class with helper functions
class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	# create a jinja template from a file
	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("index.html")

    def post(self) :

    	nombre = self.request.get("nombre")
    	password = self.request.get("password")
    	error = "Debes llenar todos los campos"

    	if nombre and password :

    		pass

    	else :

    		self.render("index.html", error=error)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
