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
from google.appengine.ext import db


# setting the dir of the template = actual pos + templates
template_dir = os.path.join(os.path.dirname(__file__), 'Crud_templates')
# setting jinja enviroment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape=True) # autoscape

class Persona(db.Model) :

    nombre = db.StringProperty()
    edad = db.IntegerProperty()

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

    pass

class RegisterHandler(Handler) :

    def get(self) :

        self.render("crud.html")

    def post(self) :

        nombre = self.request.get("nombre")
        edad = self.request.get("edad")

        if nombre and edad :

            edad = int(edad)
            p = Persona(nombre=nombre, edad=edad)
            p.put()
            self.redirect("/")
        else :

            self.render("crud.html", error="Debes llenar todos los campos")


class UpdateHandler(Handler) :

    def get(self) :

        self.render("update.html")

    def post(self) :

        nombre = self.request.get("nombre")
        edad = int(self.request.get("edad"))

        if nombre and edad :

            p = Persona(nombre=nombre, edad=edad)

            p.key.delete()

        else :

            self.render("update.html", "Debes llenar todos los campos")

class DeleteHandler(Handler) :

    pass


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler),
    ('/update', UpdateHandler),
    ('/delete', DeleteHandler)
], debug=True)
