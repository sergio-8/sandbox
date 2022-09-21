import random
mano=random.sample(range(1,100 ),10)

print(mano)

for x in range(1,len(mano)):

    carta=mano[x]
    indice_uno_prima=x-1

    while indice_uno_prima >= 0 and mano[indice_uno_prima]>carta:
        mano[indice_uno_prima+1]=mano[indice_uno_prima]
        indice_uno_prima=indice_uno_prima-1

    mano[indice_uno_prima+1]=carta

print(mano)




