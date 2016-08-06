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

template_dir = os.path.join(os.path.dirname(__file__), 'blog_templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class Blog(db.Model, Handler) :

	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	date = db.DateProperty(auto_now_add = True)
	# auto now is for overwriting a existed date if it exits
	last_modified = db.DateProperty(auto_now = True)

	# this function is to convert spaces to line breaks
	def line_break(self) :
		self._render_text = self.content.replace("\n", "<br>") 
		return self.render_str("blog.html", post = self)



class BlogHandler(Handler) :

	def get(self) :

		lista_post = db.GqlQuery("SELECT  * FROM Blog order by date desc limit 10 ")
		self.render("blog.html", lista_post = lista_post)


class NewPostHandler(Handler) :

	def get(self) :

		self.render("newpost.html")

	def post(self) :

		subject = self.request.get("subject")
		content = self.request.get("content")

		error = ""


		if subject and content :

			post = Blog(subject = subject, content = content)
			post.put()
			# redirecting with the key of the new post
			self.redirect('/%s' % str(post.key().id()))
		else :

			error= "YOU MUST FILL ALL THE FIELDS" 

			self.render("newpost.html", error = error, 
										subject = subject,
										content  = content)

class PostPage(BlogHandler):
    def get(self, post_id):
    	# create key from id
        key = db.Key.from_path('Blog', int(post_id))
        # obtain the model from the key
        post = db.get(key)

        if not post:
            self.write("ERRROR 404 NOT FOUND THIS PAGE WAS NOT FOUND IN THIS SERVER")
            return
        self.render("permalink.html", post = post)

app = webapp2.WSGIApplication([
    ('/', BlogHandler),
    ('/newpost', NewPostHandler),
    # passing regular expression to accept anything
    ('/([0-9]+)', PostPage)
], debug=True)
