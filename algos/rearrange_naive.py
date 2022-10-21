import random
from  typing import  List

list= random.sample(range(1,100), 20)
print(list)

def naivety(A:List[int]) -> None:

    sub=[]
    par=[]
    uber=[]
    new_A=[]

    key= int(len(A)/2)
    print(key)
    print(A[key])

    for item in A:
        if item <A[key]:
            sub.append(item)
        elif item>A[key]:
            uber.append(item)
        else:
            par.append(item)



    print('sub: ',sub)
    print('par ', par)
    print('uber ', uber)
    #print('sub :', sub, n\, 'par:', par, n\, 'uber:' uber )

    new_A=sub+par+uber



    return new_A

print(naivety(list))
