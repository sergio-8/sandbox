"""
Python Data Structures - A Game-Based Approach
Stack challenge
Robin Andrews - https://compucademy.net/
"""

import stack

string = "gninraeL nIdekniL htiw tol a nraeL"
reversed_string = ""
s = stack.Stack()

for item in string:
    s.push(item)



while s.is_empty() == False:
     for items in string:
         reversed_string += s.pop()



#print(s)
# Your solution here.

print(reversed_string)
