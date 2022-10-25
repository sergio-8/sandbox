import random
from  typing import  List

list= random.sample(range(1,100), 20)
print(list)

def dutch_flag_partition(pivot_index:int, A:List[int])-> None:
    pivot = A[pivot_index]
    for x in range (len(A))