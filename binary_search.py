import random

lista=random.sample((0,1000), 1000)


def binary_search( list, number):
    low=0
    high=len(list)

    while low < high:

        #preparing splitting mechanism

        mid=(low+high)/2
        guess= list[mid]

        #iterating on the search/split/repeat

        if guess== mid:
            return mid
        if guess<number:
            low=mid + 1
        if guess>number:
            high=mid -1
    return (print ("sorry number not in list")



binary_search(lista, 15)
