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


form_html="""
<form>
<h2>Add a food</h2>
<input type="text" name="food">
<!-- hidden inputs -> For add extra values to a get request
<input type="hidden" name="food" value="eggs">
<button>Add</button>
</form>

"""

# helper class with helper functions
class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

# normal class that inherit from handler 
class MainHandler(Handler) :

	def get(self) :

		self.write(form_html)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
