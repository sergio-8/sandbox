from typing import List


class Solution:
    def maxArea(self, heights: List[int]) -> int:

        alpha = 0
        omega = len(heights)-1

        area = 0

        while alpha < omega:

            
            shorter = heights[alpha]
            if heights[omega] < shorter:
                shorter = heights[omega]

            x = shorter * (omega-alpha)
            if area ==0 or area < x :
                area = x

            if heights[alpha] == shorter:
                 alpha = alpha+1 

            elif heights[omega]== shorter :
                omega= omega-1


        return area    


sol = Solution()

print(sol.maxArea([1,8,6,2,5,4,8,3,7])) 

            


        

        