import cgi

def escape_html(s):

	return cgi.escape(s, quote = True)


def rot13(string) :

	#string = escape_html(string)
	aux = ""

	for i in string :

		if ord(i) >= 97 and ord(i) <= 109 :

			aux += chr(ord(i) + 13)
			continue

		if ord(i) >= 110 and ord(i) <= 122 :

			aux += chr(ord(i) - 13)
			continue

		if ord(i) >= 65 and ord(i) <= 77 :

			aux += chr(ord(i) + 13)
			continue

		if ord(i) >= 78 and ord(i) <= 90 :

			aux += chr(ord(i) - 13)
			continue

		aux += i

	aux = escape_html(aux)

	return aux


print rot13("")






