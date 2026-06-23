import random 
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:

      low =0 
      high=len(nums)-1
      mid = (low+high) //2

      while low <= high:

        for x in range(1,len(nums)-1):
          if target > nums[mid]:
            low = mid+1
            mid =(low+high)//2
          elif target< nums[mid]:
            high = mid-1 
            mid = (low+high)//2
          else:
            return mid
      
      return None


sol = Solution()

bubba =random.randint(1, 100)
bobba =random.sample(range(1, 100),20)
bobba= sorted(bobba)
sol.search(bobba, bubba)

print("primo index is: ", sol.search(bobba, bubba), )
