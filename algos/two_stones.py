from typing import List

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        
        

        while (len(stones)) > 1:

            sto=sorted(stones)
            omega =(len(stones)-1)
            alpha = omega-1 

            diff = sto[omega]-sto[alpha]

            if diff == 0: 
                del sto[alpha:omega]
                stones=sto

            
            else:
                sto.pop()
                sto[alpha]=diff

                stones=sto

        return stones[0] if stones else 0




sol = Solution()

stones = [2,7,4,1,8,1]
print(sol.lastStoneWeight(stones))  