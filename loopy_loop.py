
import random
x=random.sample (range(1,100), 5)
pari=0
conto_pari=0
dispari=0
conto_dispari=0

for a in x:
    if a % 2==0:
        pari = pari + 1
        conto_pari= conto_pari+a
        print (a,  " mi ceppo e' pari")

    elif a %2 != 0 :
        conto_dispari= conto_dispari + a
        dispari = dispari +1
        print (a,  " moccolo e' dispari")



print ('mi ecco moccolo...')

print ('pari: ', pari, '\ndispari', dispari)
print ('pari_average: ', conto_pari/pari, '\ndispari_average :', conto_dispari/dispari)
