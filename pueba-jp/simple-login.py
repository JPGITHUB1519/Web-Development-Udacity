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

# import database
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'login_template')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)



class Handler(webapp2.RequestHandler) :
	# for counts the registers of a database
	def count(self, gql_list) :

		cont = 0;

		for obj in gql_list :

			cont = cont + 1
		return cont

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class User(db.Model) :

	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)


class MainHandler(Handler):

	def get(self):

		self.render("login.html")
		
	
	def post(self) :

		username = self.request.get("username").upper()
		password = self.request.get("password").upper()
		error_empty = "Debes Llenar todos los campos"
		error_exits = "Error de Usuario o Password"

		# validate
		if username and password :

			cmd = "SELECT * FROM User where username = '" + username + "' and password = '" + password + "'"
			list_users = db.GqlQuery(cmd)
			# if user was found
			if(self.count(list_users)) > 0 :

				self.render("welcome-login.html", username = username)

			else :

				self.render("login.html", error_exits = error_exits,
										  username = username)

		else :
			self.render("login.html", error_empty = error_empty, 
									  username = username)

class Signup(Handler) :

	def get(self) :

		self.render("signup.html")

	def post(self) :

		username = self.request.get("username").upper()
		password = self.request.get("password").upper()
		error_empty = "Debes llenar todos los campos"
		error_exits = "Este Usuario Ya existe"
		cond_found = False

		# validate
		if username and password :

			list_users = db.GqlQuery("SELECT * FROM User where username = '" + username + "'")

			# si no encotro ese usuario
			if self.count(list_users) > 0 :

				self.render("signup.html", error_exits = error_exits)

			else :

				# save user in database
				# set keyname equal to username
				user = User(username = username, password = password, key_name = username)
				user.put()

				self.redirect("/welcome?" + ("username=" + username))

		else :

			self.render("signup.html", error_empty = error_empty)

class WelcomeSignup(Handler) :

	def get(self) :

		username = self.request.get("username")
		self.render("welcome.html", username = username)

class WelcomeLogin(Handler) :

	def get(self) :

		username = self.request.get("username")
		self.render("welcome-login.html", username = username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup),
    ('/welcome', WelcomeSignup),
    ('welcome-login', WelcomeLogin)
], debug=True)
