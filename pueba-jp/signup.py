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
import cgi
import re

# validation variables

user_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_check = re.compile(r"^.{3,20}$")
email_check = re.compile(r"^[\S]+@[\S]+.[\S]+$")


form="""
<form method="post" action="/">
	
	<label>
		Day
		<input type="text" name="day" value="%(day)s"> 
	</label>	

	<label>
		Month
		<input type="text" name="month" value="%(month)s">
	</label>

	<label>
		Year
		<input type="text" name="year" value="%(year)s">
	</label>

	<input type="submit">
	<div style="color : red;">%(error)s</div>
</form>
"""

form_rot13 = """
<form method="post" action="/rot13">
	<h1>Enter Some text to ROT13</h1>
	<textarea name="text" rows="5" cols="20">%(text)s</textarea>
	<br>
	<input type="submit">

</form>
"""

form_signup = """
<html>
<head>
<style>
	.error
	{
		color:red;
	}
</style>
</head>
<body>
	<form method="post" action="/signup">
		<h2>Signup</h2>
		<label>Usuario</label><input type="text" name="usuario" value="%(valor_usuario)s"><span class="error">%(error_usuario)s</span>
		<br>
		<label>Password</label><input type="password" name="password"><span class="error">%(error_password)s</span>
		<br>
		<label>Verify Password</label><input type="text" name="verify_password"> <span class="error">%(error_verify_password)s</span>
		<br>
		<label>Email</label><input type="text" name="email" value="%(valor_email)s"><span class="error">%(error_email)s</span>
		<br>
		<input type="submit">
	</form>
</body>
</html>

"""
welcome_page = """<!DOCTYPE html>
<html>
<head>
	<title>Bienvenido %(usuario)s !</title>
</head>
<body>

	<p>Bienvenido %(usuario)s</p>

</body>
</html>"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(month):

     if month == "" :

          return None

     month = month.lower()
     aux = ""
     aux = month[0].upper()
     aux = aux + month[1 : len(months)]

     if aux in months :

          return aux
     else : 

          return None

def valid_day(day):

	if day and day.isdigit() :

		aux = int(day)

		if aux > 0 and aux <= 31 :

			return aux

		return None

def valid_year(year):

	if year and year.isdigit() :

		aux = int(year)

		if aux >= 1900 and aux <= 2020 :

			return aux

		return None


def rot13(string) :

	#string = escape_html(string)
	aux = ""

	for i in string :

		if ord(i) >= 97 and ord(i) <= 109 :

			aux += chr(ord(i) + 13)
			continue

		if ord(i) >= 110 and ord(i) <= 122 :

			aux += chr(ord(i) - 13)
			continue

		if ord(i) >= 65 and ord(i) <= 77 :

			aux += chr(ord(i) + 13)
			continue

		if ord(i) >= 78 and ord(i) <= 90 :

			aux += chr(ord(i) - 13)
			continue

		aux += i

	aux = escape_html(aux)

	return aux

def validate_usuario(usuario) :

	return user_check.match(usuario)

def validate_password(password) :

	return password_check.match(password)

def validate_email(email) :

	return email_check.match(email)

def escape_html(s):

	return cgi.escape(s, quote = True)

class MainHandler(webapp2.RequestHandler):

	def write_form(self, error="", day="", month="", year="") :

		self.response.out.write(form % {"error" : escape_html(error),
										"day" : escape_html(day),
										"month" : escape_html(month),
										"year" : escape_html(year)})

	def get(self):
	    self.write_form()

	def post(self) :
		day = self.request.get("day")
		month = self.request.get("month")
		year = self.request.get("year")

		if not(valid_day(day) and valid_month(month) and valid_year(year)) :
			self.write_form("This is an invalid Date",  day, month, year)
		else :
			
			#redirection to the other page
			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler) :

	def get(self) :

		self.response.out.write("Thanks Thats a valid Date!")

class Rot13Handler(webapp2.RequestHandler) :

	def write_form(self, text="") :

		self.response.out.write(form_rot13 % {"text" : text})

	def get(self) :

		self.write_form()

	def post(self) :
		text = self.request.get("text")
		self.write_form(rot13(text))

class SignUpHandler(webapp2.RequestHandler) :

	def write_form(self, error_usuario="", error_password="", 
				   error_verify_password="", error_email="", valor_usuario="",
				   valor_email = "") :

		self.response.out.write(form_signup % {"error_usuario" : error_usuario,
											   "error_password" : error_password,
											   "error_verify_password" : error_verify_password,
											   "error_email": error_email,
											   "valor_usuario" : valor_usuario,
											   "valor_email" : valor_email})

	def get(self) :

		self.write_form()

	def post(self) :

		# obteniendo datos del request
		usuario = self.request.get("usuario")
		password = self.request.get("password")
		verify_password = self.request.get("verify_password")
		email = self.request.get("email")

		# variables para almacenar los errores
		error_usuario = ""
		error_password = ""
		error_verify_password = ""
		error_email = ""
		cond_error = False

		# validando
		if not validate_usuario(usuario) :

			error_usuario = "That's not a valid usuario."
			cond_error = True

		if not validate_password(password) :

			error_password = "That wasn't a valid password."
			cond_error = True

		else :

			if password != verify_password :

				error_verify_password = "Your passwords didn't match."
				cond_error = True

		if email != "" :

			if not validate_email(email) :

				error_email = "That's not a valid email."
				cond_error = True

		if not cond_error :

			# enviar datos como si fuera un get request
			self.redirect("/welcome?usuario=" + usuario)
		
		else :

			self.write_form(error_usuario, error_password, error_verify_password, error_email, usuario, email)

class welcomeHandler(webapp2.RequestHandler):

	def write_form(self, usuario="") :

		self.response.out.write(welcome_page % {"usuario" : usuario})

	def get(self) :

		usuario = self.request.get("usuario")
		self.write_form(usuario)


"""
class FormHandler(webapp2.RequestHandler) :

	def get(self) :

		# get value from the request line
		#q = self.request.get("q")
		self.response.write(self.request)
"""

# reading data day = self.response.request.get("day")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler),
    ('/rot13', Rot13Handler),
    ('/signup', SignUpHandler),
    ("/welcome", welcomeHandler)
    #('/Form', FormHandler) #adding a handler 
], debug=True)
