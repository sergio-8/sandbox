import random

lista= random.sample(range(1,50),10)
print(lista)

def insort(arr):

    for x in range (1 , len(arr)):
        key=arr[x]
        y=x-1

        while y>=0  and arr[y]>key:
            arr[y+1]=arr[y]
            print(arr)
            y=y-1
        arr[y+1]= key

    print(arr)

insort(lista)



