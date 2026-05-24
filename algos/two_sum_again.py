from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        x = 0
        
        for x in range(len(nums)-1):
            for y in range (x+1, len(nums)):
        
                if nums[x]+nums[y]==target:
                    return[x,y]
                else:
                    y+1
        return None


eccolo=Solution()

print(eccolo.twoSum([2, 7, 11, 15], 18))
