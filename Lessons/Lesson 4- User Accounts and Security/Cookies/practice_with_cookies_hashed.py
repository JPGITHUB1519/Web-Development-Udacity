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
import hashlib

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)


# make a new hashing string
def hash_str(s):
    return hashlib.md5(s).hexdigest()

# make a string with the format value,hash
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

# check if a string with the format value-hash is correct
def check_secure_val(h):
    ###Your code here

    lista = h.split('|')

    if hash_str(lista[0]) == lista[1] :

    	return lista[0]

    return None


class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        # cookies must be string
    	# obtaining the value from cookies dictionary and checking that has the correct hashed value
    	cont = check_secure_val(self.request.cookies.get("cont"))

        # if has any value or has a valid hashed valued
    	if cont :
    		cont = int(cont) + 1
    	else :
    		cont = 0
    		cont = cont + 1

    	if cont >= 30 :
    		self.write("WOW, YOU ARE THE BEST : " + str(cont))
    	
    	self.write(cont)
        # making a secure cookie
    	cont = make_secure_val(str(cont))
        #saving cookie in the client
    	self.response.set_cookie("cont", cont)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
