import random

arr=random.sample(range(0,100),50)
print(arr)

def qs(arg):
    if len(arg)<2:
        return arg

    else:
        ceppo=arg[0]
        sopra=[x for x in arg[1:] if x > ceppo]
        sotto=[x for x in arg[1:] if x < ceppo]
        return qs(sotto)+[ceppo]+qs(sopra)


print(qs(arr))
