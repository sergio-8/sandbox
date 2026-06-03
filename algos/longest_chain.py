import random
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        
        numeri = set(nums)
        #print(numeri)
        longest = 0
        longest_seq = []

        for x in nums:
            if x-1 not in numeri:
                temp=0
                seq= []
                seq.append(x)

                while  x+1 in numeri:
                    seq.append(x+1)
                    x = x+1

                
            


                    

                temp=len(seq)
                if temp>longest:
                    longest=temp
                    longest_seq = seq

                
        return longest, longest_seq
        
        



sol = Solution()
nums =random.sample (range(1,100),30)
length , sequence = sol.longestConsecutive(nums)
print(f"Length: {length}")
print(f"Sequence: {sequence}")


