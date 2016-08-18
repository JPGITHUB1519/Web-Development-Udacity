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
import re
import random
import string
import hashlib

# import database
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'blog_templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)

# global variables

# validation variables
user_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_check = re.compile(r"^.{3,20}$")
email_check = re.compile(r"^[\S]+@[\S]+.[\S]+$")

# global functions

# count registers

def count_registers(dataset) :
	cont = 0
	for i in dataset :
		cont = cont + 1
	return cont

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# make password hash
def generate_hash(name, pw, salt) :
	return hashlib.sha256(name + pw + salt).hexdigest()

# this is the method to generate a hash to the user and password
def make_pw_hash(name, pw):
    salt = make_salt()
    h = generate_hash(name, pw, salt)
    return '%s,%s' % (h, salt)

# verify if hash mash with a user 
def valid_pw(name, pw, h):
    obtain_salt = h.split(',')[1]
    test_h = generate_hash(name, pw, obtain_salt) + "," + obtain_salt
    if  test_h == h :
    	return True
    return False


def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    lista = h.split('|')

    if hash_str(lista[0]) == lista[1] :

    	return lista[0]

    return None

# def password_hasher(id, hash) :
# 	string = id + "|" + hash

# main handler
class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

# models
class User(db.Model) :
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	date = db.DateProperty(auto_now_add = True)


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

class SignUpHandler(Handler):

	def validate_usuario(self, usuario) :
		return user_check.match(usuario)

	def validate_password(self, password) :
		return password_check.match(password)

	def validate_email(self, email) :
		return email_check.match(email)

	def get(self) :

		self.render("signup.html")

	def post(self) :
		# obteniendo datos del request
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		# variables para almacenar los errores
		error_user = ""
		error_password = ""
		error_verify = ""
		error_email = ""
		error_exists = ""
		cond_error = False

		# validando
		if not self.validate_usuario(username) :
			error_user = "That's not a valid usuario."
			cond_error = True

		# check if the ingresed user exits in the database
		user_list = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" % username)
		if count_registers(user_list) > 0 :
			error_exists = "This User Already Exits in the Database"
			cond_error = True


		if not self.validate_password(password) :
			error_password = "That wasn't a valid password."
			cond_error = True
		else :
			if password != verify :
				error_verify = "Your passwords didn't match."
				cond_error = True
		if email != "" :
			if not self.validate_email(email) :
				error_email = "That's not a valid email."
				cond_error = True

		if not cond_error :
			# look for if the user exits
			
			# si no hay error
			password = make_pw_hash(username, password)
			user = User(username = username, password = password)
			user.put()
			# generating a cookie for the user
			user_cookie =  make_secure_val(str(user.key()))
			#self.write(user_cookie)
			self.response.set_cookie('user_id', user_cookie)
			self.redirect("/welcome")
		else :
			# sending error to form
			self.render("signup.html",
							error_user= error_user, 
							error_password = error_password,
							error_verify = error_verify,
							error_email = error_email, 
							username = username, 
							email = email,
							error_exists = error_exists)

class WelcomeHandler(Handler) :

	def get(self) :
		user_cookie_value = self.request.cookies.get("user_id")
		if check_secure_val(user_cookie_value) :
			# obtain data from cookie
			aux = user_cookie_value.split("|")
			key = aux[0]
			# getting username from cookie
			user = db.get(key)

			self.render("bienvenido.html", user = user.username)
		else :
			self.redirect("/signup")

app = webapp2.WSGIApplication([
    ('/', BlogHandler),
    ('/newpost', NewPostHandler),
    # passing regular expression to accept anything
    ('/([0-9]+)', PostPage),
    ('/signup', SignUpHandler),
    ('/welcome', WelcomeHandler)
], debug=True)