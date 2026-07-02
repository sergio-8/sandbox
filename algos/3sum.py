def three_sum(nums):
    
    # Replace this placeholder return statement with your code
    nums.sort()
    alpha=0
    omega =len(nums)-2
    
    fermo=0
    
    hold= []
    
    for x in range(len(nums)):
        
        alpha=x+1
        omega =len(nums)-1
        while alpha < omega:
            
            if -(nums[alpha]+nums[omega]) == nums[x]:
                
                new= [nums[alpha],nums[omega],nums[x] ]
                if new not in hold :
                    hold.append(new)
                alpha = alpha +1 
                omega = omega-1 

            elif -(nums[alpha]+nums[omega])>nums[x]:
                alpha = alpha+1 
                
            
            else:
                omega = omega-1 
            

          
    
    
    return hold


bongo=three_sum([-1, 0, 1, 2, -1, -4])
print(bongo)
bongo=three_sum([0, 0, 0, 0, 0, 0, 0])
print(bongo)    

bongo=three_sum([-1,-1,-1,0,1,1,1,2,2])
print(bongo)

