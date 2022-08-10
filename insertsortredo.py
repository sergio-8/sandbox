import random

list = random.sample(range(10,1000),10)

print(list)



for indice in range  (1, len(lista)):

    carta=lista[indice]
    indice_a_sinistra=indice-1
    carta_sinistra=lista[indice_a_sinistra]


    while indice_a_sinistra > 0 and carta_sinistra>carta:
        lista[indice_a_sinistra+1]=lista[indice_a_sinistra]
        indice_a_sinistra=indice_a_sinistra-1

    lista[indice_a_sinistra+1]=lista[indice]

print(lista)


















for x in range (len(list)):

    key= list[x]
    key_minus_one=x-1

    while key>0 and list[key_minus_one] > key:













    if list[x]<list[x-1]:

        list[x-1]=lis

        key=
