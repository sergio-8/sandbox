class Solution:
    def maxProfit(self, prices) -> int:
        prof=0
        x=0
        
        
        
        for x in range(len(prices)-1) :
            y=len(prices)-1
            while y > x:
                delta = prices[y] - prices[x]
                if prof is None :
                    prof = delta
                elif prof<delta:
                    prof=delta
                y = y-1
            
        return prof
        
sol= Solution()
print(sol.maxProfit(prices = [10,1,5,6,7,1]))

