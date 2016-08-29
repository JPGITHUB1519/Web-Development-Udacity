from xml.dom import minidom

# string to XML
x = minidom.parseString("<mytag><children><item>1</item><item>2</item></children></mytag>")

# beautiful XML
print x.toprettyxml()

print x.getElementsByTagName("item")[0].childNodes[0].nodeValue

# all get a list of the elements
# get all items value
for i in x.getElementsByTagName("item") :

	for j in i.childNodes :

		print j.nodeValue


