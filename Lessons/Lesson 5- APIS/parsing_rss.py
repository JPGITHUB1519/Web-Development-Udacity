import urllib2
from xml.dom import minidom



x = urllib2.urlopen("http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml")

xml =  minidom.parseString(x.read())

print x.read()
# getting the numbers of items tag
num = len(xml.getElementsByTagName("item"))

print num
