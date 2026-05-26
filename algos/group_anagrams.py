from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        gruppo_anagr = {}
        
        

        
        
        
        for x in strs:
            conto=[0]*26
            for char in x:
                indice = ord(char) - ord('a') 
                conto[indice] += 1
            
            sign = tuple(conto)

            if sign in gruppo_anagr:
                gruppo_anagr[sign].append(x)
            else:
                gruppo_anagr[sign]=[x]
        return list(gruppo_anagr.values())


eccolo = Solution()
abc = eccolo.groupAnagrams(strs=["act", "pots", "tops", "cat", "stop", "hat"])
print(abc)
