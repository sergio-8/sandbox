import random
from  typing import  List

list= random.sample(range(1,100), 10)
print(list)

def dutch_flag_partition(pivot_index:int, A:List[int])-> None:
    pivot = A[pivot_index]
    print(pivot)
    #r = 0
    for x in range (len(A)):
        print(f'start base loop, x is {A[x]}')
        r = 1


        for y in range (x+1, len(A)):
            print('start nested loop')

            print(f'nested loop round {r} , y is {A[y]}')
            r+=1

            if A[y]<pivot:
                print('about to enforce swap round', r)
                A[x], A[y] =A[y], A[x]
                print('swapped A =', A)
                
                break
    print('status mid process: ', A)

    for z in reversed (range (len(A))):
        print('start reverse base loop')
        for zap in  reversed (range (z)):
            print('reverse nested loop')
            if A[zap]> pivot:
                print('about to enforce reverse swap round', r)
                A[z], A[zap]= A[zap], A[z]
                print('swapped A =', A)
                break



    print (A)


dutch_flag_partition(5, list)