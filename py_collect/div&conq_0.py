import random

lista=list(range(2,9))
print(lista)


class solution():
    sum = 0

    def __init__(self, arr):
        self.arr= arr

    def somma(self):
        for x in self.arr:
            sum += x
        return sum

s=solution(lista)
print(s.somma())

