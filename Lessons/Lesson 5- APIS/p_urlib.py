import urllib


p = urllib.urlopen("https://www.udacity.com/")

print p.read()