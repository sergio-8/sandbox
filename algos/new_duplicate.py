from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:

        dups= {}

        for x in nums:

            if x in dups:
                return True



            if x not in dups:
                dups[x]=1

        return False


sol=Solution()
print(sol.hasDuplicate([1,2,3,4,5,6,7,8,9,10,1]))


