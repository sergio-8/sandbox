import random
from typing import List

test=random.sample (range(1,100),15)
print(test)


def even_odd(A: List[int]) -> None:
    # TODO - you fill in here.
    n_even, n_odd = 0, len(A)-1
    while n_even < n_odd:
        if A[n_even] % 2 == 0:
            n_even += 1
        else:
            A[n_even], A[n_odd]= A[n_odd],A[n_even]
            n_odd -= 1

    return A


c = even_odd(test)
print(c)