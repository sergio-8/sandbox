def find_duplicate(nums):

    # Replace this placeholder return statement with your code
    
    l = 0
    v = 0
    
    lento = nums[l]
    veloce = nums[nums[v]] 
    
    while lento != veloce : 


        lento = nums[lento]
        veloce = nums[nums[veloce]] 


        continue 
    
    nuovolento = 0 

    #lento = nums[l] 
    #nuovolento = nums[nuovolento]

    while nums[lento] != nums[nuovolento]:
        lento = nums[lento]
        nuovolento = nums[nuovolento] 
        continue
    

    return nums[lento]


print( find_duplicate([3,4,4,4,2]))
#print( find_duplicate([1,3,4,2,2]))

