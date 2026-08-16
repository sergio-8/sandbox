'''

Starting with the given number , replace the number with the sum of the squares of its digits.
Repeat the process until:
The number equals 1, which will depict that the given number  is a happy number.
The number enters a cycle, which will depict that the given number 
 is not a happy number.
Return TRUE if is a happy number, and FALSE if not. '''



def is_happy_number(n):

    def breakthem(n):
        #print("taking n = ", n)
        sums = sum(int(char)**2 for char in str(n))

        return sums

    slow = n
    fast= breakthem(n)

    while fast !=1 and slow != fast:

        s = breakthem(slow)
        f = breakthem(breakthem(fast))
        slow = s 
        fast = f
        continue

    return fast == 1





    #print(n)
    #print("this is squares", breakthem(n))



#print(is_happy_number(23))
#print(is_happy_number(456))
print(is_happy_number(7890))
