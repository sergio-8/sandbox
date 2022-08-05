import random
#lista=list()
num=input("scegli il numero")
num= int(num)
lista=list(range(21, 50000))

count=0
#print(type(lista))
#print( num in  lista)

low=0
high=len(lista)-1

while high>=low:

    #preparing splitting mechanism

    mid=(low+high)//2


    guess= lista[mid]
    #print(guess)

    #iterating on the search/split/repeat

    if guess== num:
        print(guess)
        break


    if guess<num:
        low=mid+1
        count=count +1
        print("guess is: ", guess , "and it's low, adjusting", count )

    else:
        count=count+1
        high=mid-1
        print("guess is: ", guess, "and it's high, adjusting" , count)

"""
    else:
        count=count+1
        print ("e ora?", count)



#binary_search(lista,num )
"""