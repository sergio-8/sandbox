import random

lista= [random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']) for _ in range(10)]

#print(lista)
gifuni={}


for a, b in enumerate(lista):
  gifuni[b] = a

print(gifuni)


  

  




