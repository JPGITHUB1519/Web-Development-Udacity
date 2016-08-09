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
			<input type="text" name="month">
		</label>

		<label>
			Day
			<input type="text" name="day">
		</label>

		<label>

			Year
			<input type="year" name="year">
		</label>


		<input type="submit">

	</form>

</body>
</html>"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	#self.response.headers['Content-Type'] = "text/plain"
        self.response.write(form)

    def post(self) :

    	self.response.write("Thanks, this is a totally valid day")



app = webapp2.WSGIApplication([
    ('/', MainHandler)],debug=True)
