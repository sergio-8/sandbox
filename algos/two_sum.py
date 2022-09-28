from typing import List
arr=[2,3,5,7,8,1,15,]
t=16

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mappa={}
        paio=[]
        x=0
        eureka=False

        while x < len(nums):
            mappa[nums[x]]=x
            x += 1
        print(mappa)
        print(mappa.keys())
        print(mappa.values())

        x = 0

        while x< len(nums) and not eureka:
            tassello= target-nums[x]
            print(tassello,'dato da',target, ' meno ', nums[x])

            if tassello in mappa:
                print('primo indice=', x,'secondo indice', mappa[tassello])
                if x != mappa[tassello]:

                    paio.append(x)
                    paio.append(mappa[tassello])
                    eureka=True
                    print('trovato')

            x +=1
        return (paio)


s = Solution()
print(s.twoSum(arr, t))