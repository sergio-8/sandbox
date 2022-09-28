from typing import List
arr=[1,2,3,5,7,8,9,]
t=13

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

        x = 0

        while x< len(nums) and not eureka:
            tassello= target-nums[x]
            print(tassello,'=',target, ' meno ', nums[x])

            if tassello in mappa:
                print('indice=', x,'valore?', mappa[tassello])
                if x != mappa[tassello]:

                    paio.append(x)
                    paio.append(mappa[tassello])
                    eureka=True
                    print('trovato')

            x +=1
        return (paio)


s = Solution()
print(s.twoSum(arr, t))