from typing import List

ceppo = [1,2,3,4,5,6,7,8,9]



def even_odd(A: List[int]) -> None:
    # TODO - you fill in here.
    next_even, next_odd= 0 , len(A)-1
    print(next_even, next_odd)
    while next_even < next_odd:
        if A[next_even] % 2 ==0:
            next_even += 1
            print(next_even, next_odd)
        else:
            A[next_even], A[next_odd] =A[next_odd], A[next_even]
            next_odd -= 1
            print(A[next_even], A[next_odd])


    return print(A), next_even, next_odd

even_odd(ceppo)
