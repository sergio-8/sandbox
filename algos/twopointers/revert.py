def is_strobogrammatic(num):
  
    # Replace this placeholder return statement with your code
    
    valid = {('0', '0'),

  
        ('1', '1'),
        
          
        ('8', '8'),
        
          
        ('6', '9'),
        
          
        ('9', '6')}
        

    
    left, right = 0, len(num)-1
    


    while left <= right:
        if (num[left], num[right]) in valid:
            left = left + 1
            right = right - 1
        else:
            return False
        
    return True
        
num = ('961196116996889696888896968888969688966911961196')

print(is_strobogrammatic(num))
    
    