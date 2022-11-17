import random
from typing import List

test=random.sample (range(1,100),15)
print(test)


def insert(A, j):
    i=j-1

    for i in range ( 1, j):
        if A[i] > A[i+1]:
            A[i], A[i+1]=A[i+1], A[i]
            print('swap')

        else:
            break


def ins_sort(A):
    for j in range (1, len(A)):
        insert(A, j)
    print(A)

ins_sort(test)

#print(run)

