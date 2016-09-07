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
from xml.dom import minidom
import urllib2

#library to debugging
import logging

# import database
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape=True)


IP_PAGE = "http://ip-api.com/xml/"
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"
def get_coords(ip) :
	# test ip
	ip = "107.22.175.13"
	url = IP_PAGE + ip
	content = None

	try :
		content = urllib2.urlopen(url)
	except :
		None

	if content :
		parse_xml = minidom.parseString(content.read())
		lat = parse_xml.getElementsByTagName("lat")[0].childNodes[0].nodeValue
		lon = parse_xml.getElementsByTagName("lon")[0].childNodes[0].nodeValue
		return db.GeoPt(lat, lon)

# generating the image from url to send to google api
def gmaps_img(points):
    ###Your code here
    base_markers= "&markers="
    markers_string = ''
    for p in points :
    	markers_string += base_markers + str(p.lat) + "," + str(p.lon)

    url = GMAPS_URL + markers_string
    return url

# hashing table for cache
CACHE = {}
# this get the most recent created arts
# update is for always has the cache full and avoid cache stampede
def top_arts(update = false) :
	# this is the key of the query in the cache
	key = "top"
	if not update or key in CACHE :
		arts = CACHE[key]
	else :
		logging.error("DB QUERY")
		# executing the query and saving the results in a variable
		# remember that in google data store we only can use select * from, all the properties
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		# prevent the running of multiples queries
		arts = list(arts)
		CACHE[key] = arts
	return arts

class Handler(webapp2.RequestHandler) :

	def write(self, *a, **kw) :

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params) :

		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw) :

		self.write(self.render_str(template, **kw))


# in appengine databases are definen by classes and are entities

class Art(db.Model) :

	# defining properties with their respective fields
	
	title = db.StringProperty(required = True) # required is a constraint like not null in sql server
	art = db.TextProperty(required = True)
	# save the date automatically
	created = db.DateTimeProperty(auto_now_add = True) 
	coords = db.GeoPtProperty()	

class MainHandler(Handler):

	# function to render the form
	# we can render with 
	def render_front(self, title="", art="", error="") :
		# getting the top 10 arts
		arts = top_arts()
		# saving who was coordenates
		points = []
		for a in arts :
			if a.coords :
				points.append(a.coords)

		# generating img url
		img_url = None
		if points :
			img_url = gmaps_img(points)

		self.render("index.html", title = title, art = art, error = error, arts=arts, img_url=img_url)

	
	def get(self):
		self.render_front()
	
	def post(self) :
		#get values
		title = self.request.get("title")
		art = self.request.get("art")
		if title and art :
			# creating a new object of the entity
			a = Art(title=title, art=art)
			# getting ip
			my_coords = self.request.remote_addr
			a.coords = get_coords(my_coords)
			# save it in the database
			a.put()
			# updating the cache only when writing
			top_arts(True)


			# # clearing the catch for get it to its original state
			# do not do this for avoid cache stampide
			# CACHE.clear()

			logging.error(CACHE)
			self.redirect(self.request.url)
		else :
			error = "We need both, the title and the art work"
			self.render_front(title, art, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
