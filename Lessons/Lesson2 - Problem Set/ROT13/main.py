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


form = """<!DOCTYPE html>
<html>
<head>
	<title>Birthday</title>
</head>
<body>

	<form method = "post">
		
		What is Your Birthday?
		<br>
		<label>
			Month
			<input type="text" name="month" value=%(month)s>
		</label>

		<label>
			Day
			<input type="text" name="day" value=%(day)s>
		</label>

		<label>

			Year
			<input type="year" name="year" value=%(year)s>
		</label>

		<div style="color:red">%(error)s</div>
		<br>
		<br>
		<input type="submit">


	</form>



</body>
</html>"""

form_rot13 = """<!DOCTYPE html>
<html>
<head>
	<title>TextArea</title>
</head>
<body>

	<form method="post">
		<label>
			<p>Escriba su Texto Aqui :</p>
			<textarea name="text">%(texto)s</textarea>
			<br>
			<input type="submit">


		</label>
	</form>

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

def escape_html(s):
	return cgi.escape(s, quote = True)  

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

def rot13(text) :

	aux = ""

	for i in text :

		i_number = ord(i)

		#lower case
		if  i_number >= 97 and i_number <= 109 :

			i_number =  i_number + 13


		elif i_number >= 110 and i_number <= 122 :

			i_number = i_number - 13

		# upper case
		elif i_number >= 65 and i_number <= 77 :

			i_number =  i_number + 13

		elif i_number >= 78 and i_number <= 90 :

			i_number =  i_number - 13

		aux += chr(i_number)

	return aux

class MainHandler(webapp2.RequestHandler):

	def write_form(self, error="", month="", day="",year="") :
		self.response.out.write(form % {"error" : error,
										"month" : escape_html(month),
										"day" : escape_html(day),
										"year" : escape_html(year)})

	def get(self):
		#self.response.headers['Content-Type'] = "text/plain"
		self.write_form()
		
	def post(self) :

		user_month = self.request.get("month")
		user_day = self.request.get("day")
		user_year = self.request.get("year")

		month =  valid_month(self.request.get("month"))
		day = valid_day(self.request.get("day"))
		year = valid_year(self.request.get("year"))

		if not(month and day and year) :

			self.write_form("Thats does not look valid to me, friend", user_month, user_day, user_year)

		else :

			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler) :

	def get(self) :

		self.response.out.write("Thanks, this is a totally valid day")

class Rot13Handler(webapp2.RequestHandler) :

	def write_form(self, texto="") :

		self.response.out.write(form_rot13 % {"texto":texto})



	def get(self) :

		self.write_form()

	def post(self) :

		text = self.request.get("text")
		text = rot13(text)
		self.write_form(text)

	
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/thanks', ThanksHandler), ('/unit_2/rot13', Rot13Handler)],debug=True)
