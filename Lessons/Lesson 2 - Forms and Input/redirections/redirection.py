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



"""
class FormHandler(webapp2.RequestHandler) :

	def get(self) :

		# get value from the request line
		#q = self.request.get("q")
		self.response.write(self.request)
"""

# reading data day = self.response.request.get("day")

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/thanks', ThanksHandler)
    #('/Form', FormHandler) #adding a handler 
], debug=True)
