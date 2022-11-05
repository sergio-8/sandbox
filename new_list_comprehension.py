pizze = ['rossa','bianca','marinara']

taglie = "piccola media grande".split()

numeri = [1 , 2, 3  ]

ordine = [(taglia,  pizza, numero) for pizza in pizze for taglia in taglie for numero in numeri ] +list('ACE' 'TO')

print(ordine)