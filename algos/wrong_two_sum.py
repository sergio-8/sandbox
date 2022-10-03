from typing import List
arr=[2,7,11,15]
t=9
class Solution(object):

    def twoSum(self, nums, target):
        maps = {}
        pair = []
        x = 0
        found_it = False

        while x < len(nums):
            maps[nums[x]] = x
            x += 1

        x = 0

        while x < len(nums) and not found_it:

            diff = target - nums[x]
            if diff in maps and diff != x:
                pair.append(x)
                pair.append(maps[diff])
                found_it = True
                print(pair)

            x += 1

        return pair


b=Solution()
b.twoSum(arr, t)

