import random

lista= random.sample(range(1,50),5)
#print('the way it is', lista)
lst=[31, 17, 12, 8, 3]
print(lst)

def insort(arr):
    round=1

    for x in range (1 , len(arr)):
        print('START HERE: assignin values and index for round', round)
        key=arr[x]
        print('key, its value , remember, is ', key ,'and is now located at index', x)
        y=x-1
        print('y, is just  a n index and is  = to',y, 'and has value' ,arr[y] )


        while y>=0  and arr[y]>key:
            print('in while loop for round', round, 'now ')
            arr[y+1]=arr[y]
            print('round',round,' arr of y +1 is:', arr[y+1],  arr)
            #round=round+1
            y=y-1
            print('new y index assingment', y)
            print('break')
        print('heres is the assignment out of the while loop:')
        arr[y+1]= key
        print(arr)
        round = round + 1
        print('round plus one ')


    print('final array', arr)

insort(lst)



