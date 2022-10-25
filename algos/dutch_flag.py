import random
from  typing import  List

list= random.sample(range(1,100), 20)
print(list)

def dutch_flag_partition(pivot_index:int, A:List[int])-> None:
    pivot = A[pivot_index]
    print(pivot)
    r = 0
    for x in range (len(A)):


        for y in range (x+1, len(A)):
            print('evaluating round # ', r)
            r=+1

            if A[y]<pivot:
                print('about to enforce swap round', r)
                A[x], A[y] =A[y], A[x]
                print('swapped A =', A)
                
                break

    for z in reversed (range (len(A))):
        for zap in  reversed (range (z)):
            if A[zap]> pivot:
                A[z], A[zap]= A[zap], A[z]
                break



    print (A)


dutch_flag_partition(10, list)