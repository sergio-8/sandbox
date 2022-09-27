import copy
from typing import List
import random

ceppo = [random.sample (range(1,100), 6 ),random.sample (range(1,100), 6 )]

def swap(A: List[int]):
    sx, dx = 0, len(A)-1
    print(A)
    print(A[sx], A[dx])
    A[sx], A[dx], A[sx+1], A[dx-1] =A[dx], A[sx], A[dx-1], A[sx+1]

    print(A[sx], A[dx])
    print(A)
    A.insert(3, 0)
    print(A)
    A.remove(0)
    print(type(A))

    print(A)

    B = copy.copy(A)
    print('now changing to zero')
    A[1] [0]=0
    B[0] [0]=0
    print(A,'\n', B)

    print('now inserting  a zero array')
    A.insert(1,  [0])
    B.insert(0, [0])
    print(A)
    print(B)

print(swap(ceppo))




ceppo = [random.sample (range(1,100), 6 ),random.sample (range(1,100), 6 )]

def deep_swap(A: List[int]):
    sx, dx = 0, len(A)-1
    print(A)
    print(A[sx], A[dx])
    A[sx], A[dx], A[sx+1], A[dx-1] =A[dx], A[sx], A[dx-1], A[sx+1]

    print(A[sx], A[dx])
    print(A)
    A.insert(3, 0)
    print(A)
    A.remove(0)
    print(type(A))

    print(A)

    B = copy.deepcopy(A)
    print('now changing to zero')
    A[1] [0]=0
    B[0] [0]=0
    print(A,'\n', B)

    print('now inserting  a zero array')
    A.insert(1,  [0])
    B.insert(0, [0])
    print(A)
    print(B)

deep_swap(ceppo)