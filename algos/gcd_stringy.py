import math 
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:

        hold = ""
        fuori = ""
        eccolo= math.gcd(len(str1), len(str2) )

        ceppo = str2[:eccolo]
        ceppa = str1[:eccolo]


    

        if ceppa == ceppo and ceppa * (len(str1) // eccolo) == str1 and ceppo * (len(str2) // eccolo) == str2:
            
            
            fuori = ceppo

        return fuori
        
    
        return fuori  

sol=Solution()
print(sol.gcdOfStrings("ABCABC", "ABC"))
print(sol.gcdOfStrings("ABABAB", "ABAB"))
print(sol.gcdOfStrings("LEET", "CODE")) 


    
