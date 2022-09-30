


ceppo = [1,2,3,4,5,6,7,8,9]

class Stack:

    ind=0

    def __init__(self, s):
        self.s = s
        ind = len(s)
        return None

    def __str__(self, s):
        print(self.s)

    def push(self,s,x):
        self.x=x
        ind = len(s)
        ind = ind +1
        s[ind]=self.x
        print(s)


    def pop(self):
        ind= ind-1
        return s[ind+1]
        print(s)

c = Stack(ceppo)
c.push( ceppo, 12)




