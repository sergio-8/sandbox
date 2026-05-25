from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Step 1: Taking Inventory
        # Create a dictionary and tally up the counts of each number in nums
        risultato = []
        conto = {}
        
        for x in nums:
            if x in conto:
                conto[x]+=1
            else:
                conto[x]=1
        # Step 2: Building the Bucket Array
        # Create an array of empty lists, size should be len(nums) + 1
        
        secchio = [[]for _ in range(len(nums)+1)]



        
        # Drop the numbers into the buckets based on their count
        for num, freq in conto.items():
            secchio[freq].append(num)

        
        # Step 3: Walking Backward
        # Create a result list
        # Walk backward through the bucket array, grabbing numbers until you have k numbers
        
        
        for y in range(len(secchio)-1,0,-1):
            for num in secchio[y]:
                risultato.append(num)
                if len(risultato)==k:
                    return risultato
        
        return risultato

# Test it out!
eccolo = Solution()
print(eccolo.topKFrequent([1, 1, 1, 2, 2, 3], 2)) # Should output [1, 2]
