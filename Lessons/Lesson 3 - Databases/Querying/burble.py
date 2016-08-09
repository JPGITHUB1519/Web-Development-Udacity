
lista = [5,1,4,3,2]


for i in range(0, len(lista) - 1):

	for j in range(0, len(lista) - 1) :

		if lista[j] > lista[j + 1] :

			aux = lista[j]
			lista[j] = lista[j + 1]
			lista[j + 1] = aux

print lista
