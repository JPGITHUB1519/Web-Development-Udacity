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
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'to_do_templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class task(db.Model) :

	name = db.StringProperty(required = True)
	description = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	isdone = db.BooleanProperty()


class new_task(Handler) :

	def get(self) :

		self.render("newtask.html")

	def post(self) :

		name = self.request.get("name")
		description = self.request.get("description")

		t = task(name=name, description=description, isdone=False)
		t.put()
		self.redirect("/")

class taks(Handler) :

	def get(self) :

		task_list = db.GqlQuery("SELECT * FROM task")
		self.render("task.html", task_list=task_list)


class MainHandler(Handler):
    def get(self):
        self.render("task.html")

app = webapp2.WSGIApplication([
	('/', taks),
    ('/newtask', new_task)
], debug=True)
