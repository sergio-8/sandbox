import random

lst = list(range(2, 10))

print(lst, len(lst))

for item in range (len(lst)):
    lst[item]*=3
    print(item)

print(lst, len(lst))
