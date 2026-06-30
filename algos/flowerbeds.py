from typing import List

class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        
        conto = 0 
        x= 0
        
        while x < len(flowerbed) :





            if flowerbed[x] == 0 and (x == 0 or flowerbed[x-1] ==0) and (x == len(flowerbed)-1 or flowerbed[x+1] ==0):
                conto = conto +1
                
                flowerbed[x]=1
            
            x= x+1


        if conto >= n :

            return True
        
        else:
            return False


sol=Solution()
print(sol.canPlaceFlowers([1,0,0,0,1], 1))  
print(sol.canPlaceFlowers([0,0,1,0,0], 2))
print(sol.canPlaceFlowers([1,0,0,0,0,1], 2))
print(sol.canPlaceFlowers([1,0,0,0,0,0,0,1,0,0,0,0,0,1], 3))
