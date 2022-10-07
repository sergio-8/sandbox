import random

lista= random.sample(range(1,50),10)
lst =[39, 37,18, 12,9]

print(lst)

def insort(arr):

    for x in range (1 , len(arr)):
        key=arr[x]
        y=x-1
        round=1

        while y>=0  and arr[y]>key:
            print('holding key value, assigning right to key location and moving y one position left round:', round)
            arr[y+1]=arr[y]
            print(arr)
            y=y-1
            round=round+1
        print('actual "key value" insertion now:')
        arr[y+1]= key
        print(arr)

    print(arr)
\
insort(lst)



