import random 
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:

        alpha = 0
        omega = len(nums)-1
        


        while alpha <= omega:

            middle = int (alpha+omega)//2

            if target == nums[middle]:
                return middle
            elif target < nums[middle]:
                 
                omega = middle -1

            else:

              if target > nums[middle]:
                alpha = middle +1

            # else:

            #   return int(-1)

        return int(-1)


sol = Solution()

bubba =random.randint(1, 100)
bobba =random.sample(range(1, 100),50)
bobba.sort()

#print(f"bobba is {bobba}")
#print(f"bubba is {bubba}")
print("primo index is: ", sol.search(bobba, bubba), )


bubba =random.randint(1, 100)
bobba =random.sample(range(1, 100),50)
bobba.sort()
print("secondo  index is: ", sol.search(bobba, bubba), )

print("terzo index is: ", sol.search([-1,0,2,4,6,8],4) )