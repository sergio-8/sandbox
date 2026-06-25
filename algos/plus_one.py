from  typing  import List 


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:

        hold = len(digits) -1

        for x in range(len(digits)):
            if digits[hold]  < 9 :
                digits[hold]= digits[hold]+1
                return digits 
            elif digits[hold] == 9:
                digits[hold] = 0
                hold = hold-1
        
        if digits[0]==0:
            #digits[0] = 0
            digits = [1] + digits
        
        

        return digits


sol= Solution()
questo= sol.plusOne(digits=[1,2,3,4])
print (questo)