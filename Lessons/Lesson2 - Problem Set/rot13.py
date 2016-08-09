
def rot13(text) :

	aux = ""

	for i in text :

		i_number = ord(i)

		#lower case
		if  i_number >= 97 and i_number <= 109 :

			i_number =  i_number + 13


		elif i_number >= 110 and i_number <= 122 :

			i_number = i_number - 13

		# upper case
		elif i_number >= 65 and i_number <= 77 :

			i_number =  i_number + 13

		elif i_number >= 78 and i_number <= 90 :

			i_number =  i_number - 13

		aux += chr(i_number)

	return aux



	#text = ord(text) + 13
	#return chr(text)



