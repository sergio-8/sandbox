from typing import List
import random

ceppo = random.sample (range(1,100), 20 )

def arro (A: List[int]):

    sx, dx= 0, len(A)-1
    print( 'at this point arry is ',  (A))
    print(sx,dx)
    print(A[sx], A[dx])
    while sx<dx:
        if A[sx]%2 ==0:
            sx +=1
            print('sx+1 is:')
            print(sx, dx)
        else:
            print('swap 1 update')
            A[sx], A[dx] = A[dx], A[sx]
            print(' new index #s are :')
            print(sx, dx)
            print(' new content value are :')
            print(A[sx], A[dx])
            print("updated array is :", (A))
            #print('swap 2')
            #A[dx] =  A[sx]
            #print(sx, dx)
            #print(A[sx], A[dx])
            dx -=1
            print('dx-1 is:')

            print(sx, dx)
            print(A[sx], A[dx])

    print(A)

arro(ceppo)