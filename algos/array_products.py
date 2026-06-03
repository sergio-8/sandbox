from typing import List
import random




class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        
        r_h =[]
        l_h = [0]*len(nums)
        lost=[]

        for x in range ( len(nums)):
            if x==0 :
                r_h.append(1)
            else:
                prod= r_h[x-1] * nums[x-1]
                r_h.append(prod)
        

        for y in range(len(nums) - 1, -1, -1):
            if  y== len(nums)-1:
                l_h[y]=1
            else:
                l_h[y]= l_h[y+1] * nums[y+1]
            

        for z in range (len(nums)):
            prod=r_h[z] * l_h[z]
            lost.append(prod) 

        return lost 




sol = Solution()
nums=[-1,0,1,2,3]

#nums =random.sample (range(1,100),30)
print(sol.productExceptSelf(nums))

