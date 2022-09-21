import random


arro=random.sample(range(5,100), 30)

print (arro)

def quicksort(arr):
    print(len(arr))


    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less=[x for x in arr[1:] if x <= pivot ]
        greater=[x for x in arr[1:]if x>pivot]
        return quicksort(less) +[pivot] + quicksort(greater)
    

print(quicksort(arro))