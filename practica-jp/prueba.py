import random

preguntas = {
			"Cual es el continente mas grande del mundo" : ["asia", "america" , "europa", "oceania"],
			"Cual es el continente mas pequeño del mundo" : ["europa","asia", "america" , "oceania"],
			"Cual es el continente en el que vivimos" : ["america" ,"asia", "europa", "oceania"],
			}

def generar_preguntas(max_question) :

	lista = []

	for i in range(1, max_question + 1) :

		while True :
			n = random.randint(1, max_question)
			if n not in lista :

				lista.append(n)

	return lista

				










