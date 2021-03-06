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

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))


# in appengine databases are definen by classes and are entities
# 


class Art(db.Model) :

	# defining properties with their respective fields
	
	title = db.StringProperty(required = True) # required is a constraint like not null in sql server
	art = db.TextProperty(required = True)
	# save the date automatically
	created = db.DateTimeProperty(auto_now_add = True) 
	

class MainHandler(Handler):

	# function to render the form
	# we can render with 
	def render_front(self, title="", art="", error="") :

		# executing the query and saving the results in a variable
		# remember that in google data store we only can use select * from, all the properties
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

		self.render("index.html", title = title, art = art, error = error, arts=arts)

	
	def get(self):
		self.render_front()
	
	def post(self) :
		#get values
		title = self.request.get("title")
		art = self.request.get("art")


		if title and art :

			# creating a new object of the entity
			a = Art(title=title, art=art)
			# save it in the database
			a.put()

			self.redirect("/")


		else :

			error = "We need both, the title and the art work"
			self.render_front(title, art, error)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
