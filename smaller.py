import random

dataset=random.sample (range (-100, 100),10)

smaller=None

for x in dataset:
    if smaller is None:
        smaller = x
    if smaller > x:
        smaller = x

print (dataset, smaller)
