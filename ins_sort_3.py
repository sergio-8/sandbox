import random

list=random.sample(range(1,100),10)
print(list)

for x in range (1, len(list)):
    key=list[x]
    j=x-1

    while j>=0 and list[j] > key:
        list[j+1]=list[j]
        j=j-1

    list[j+1]=key

print(list)



