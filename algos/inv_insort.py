lst=[   3, 8, 12, 17, 31 ]
lst1=[31, 17, 12, 8, 3]
print(lst1)


def inv_insort(arr):

    for x in range (1 , len(arr)):
        key=arr[x]
        y=x-1
        while y >= 0 and arr[y] > key:
            arr[y+1]=arr[y]
            y=y-1
        arr[y+1]=key
    print(arr)

print(inv_insort(lst1))