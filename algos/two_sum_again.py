from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return None


eccolo = Solution()

# A much longer list to test!
long_nums = [4, 12, 54, 19, 8, 33, 91, 10, 42, 7, 88, 23, 65, 3, 17, 99, 14, 25]
target = 100

print(f"Finding two numbers that add up to {target}...")
result = eccolo.twoSum(long_nums, target)
print(f"Resulting indices: {result}")

if result:
    print(f"Proof: {long_nums[result[0]]} + {long_nums[result[1]]} = {target}")
