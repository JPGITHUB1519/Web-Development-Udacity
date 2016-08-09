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
# importing jinja
import jinja2
import os

# setting the dir of the template = actual pos + templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# setting jinja enviroment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


form_html="""
<form>
<h2>Add a food</h2>
<input type="text" name="food">
%s
<input type="submit" value="Add">
</form>
"""

hidden_html = """
<input type="hidden" name="food" value="%s">
"""

items_html = "<li>%s</li>"


shopping_list_html = """
<br>
<br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""

# helper class with helper functions
class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	# create a jinja template from a file
	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

# normal class that inherit from handler 
class MainHandler(Handler) :

	def get(self) :

		#things comes like string in the request
		n = self.request.get("n")

		# converting into string
		if n and n.isdigit():
			n = int(n)
			self.render("shopping_list.html", n=n)
		# output = form_html
		# # to save all the output hidden with the values of the food
		# output_hidden = ""

		# # save in a list all the values of food in the get parameters
		# items = self.request.get_all("food")

		# if items : 
		# 	output_items = ""
		# 	for item in items :
		# 		#adding to the variable each one of the hidden html to the foods values
		# 		output_hidden += hidden_html % item
		# 		# adding each elements to the ul list
		# 		output_items += items_html % item

		# 	# adding the list of elements to ul list
		# 	output_shopping = shopping_list_html % output_items
		# 	# adding to the output the shopping list
		# 	output += output_shopping

		# # adding the hidden elements
		# output = output % output_hidden
		# self.write(output)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
