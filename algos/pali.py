#from random random

def is_pali(s:str) -> bool:

    return all (s[x] == s[-(x+1)] for x in range (len(s) //2 ))



gippo= is_pali ("anna")
print(gippo)