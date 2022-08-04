import random

list = random.sample(range(10,100),10)

print (list)
#print(len(list))


for x in range(1, len(list)):
    key = list[x]
    x_minus_one_index= x-1
    #print(key, key_plus_one)

    while x_minus_one_index >= 0 and list[x_minus_one_index] > key:
        list[x_minus_one_index+1]=list[x_minus_one_index]
        x_minus_one_index=x_minus_one_index-1

    list[x_minus_one_index+1]=key

print(list)
