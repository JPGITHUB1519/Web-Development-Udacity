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

class MainHandler(webapp2.RequestHandler):

	def write_form(self, error="", month="", day="",year="") :
		self.response.out.write(form % {"error" : error},
										"month" : month,
										"day" : day,
										"year" : year)

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

			self.write_form("Thats does not look valid to me, friend", month, day, year)

		else :

			self.response.out.write("Thanks, this is a totally valid day")


app = webapp2.WSGIApplication([
    ('/', MainHandler)],debug=True)
