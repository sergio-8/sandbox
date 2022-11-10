import random
list=random.sample (range(0,10000), 10)
print(list)
sofar=-1
for x in list:
    if sofar<x:
        print("before", sofar, "now: ", x)
        sofar=x
        print (sofar)
print("the largest is: ", sofar)
