from typing import List

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        if not nums:
            return False
        nums.sort()
        print(f"Sorted nums: {nums}")
        print(f"Length of list minus 1 is: {len(nums) - 1}")
        print(f"The range to check is: {range(len(nums) - 1)}")
        for x in range(len(nums) - 1):
            if nums[x] == nums[x+1]:
                return True

        return False

# Instantiate the class
sol = Solution()

# Test Case 1: Has Duplicates
test1 = [1, 2, 3, 1]
print(f"Test 1 Input: {test1}")
result1 = sol.hasDuplicate(test1)
print(f"Test 1 Result: {result1}\n")

# Test Case 2: No Duplicates
test2 = [1, 2, 3, 4]
print(f"Test 2 Input: {test2}")
result2 = sol.hasDuplicate(test2)
print(f"Test 2 Result: {result2}")
