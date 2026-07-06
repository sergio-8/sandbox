def is_palindrome(string):
  

  alpha = 0
  omega = len(string)-1
  
  def ispal(s):
    return s == s[::-1]
    
  
  
  while alpha<omega:
    if string[alpha] == string[omega]:
      alpha = alpha +1
      omega = omega -1
  
      
  
  
    else: 
        
        left = string[alpha+1 : omega+1]
        right = string[alpha :omega]
        
        return ispal(left) or ispal(right)
   
  return True
        
        

print(is_palindrome("abca"))
print(is_palindrome("racecar"))
print(is_palindrome("aba"))
print(is_palindrome("carac"))
print(is_palindrome("bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVgVUTSRQPONMLKLJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba")) 
    
  
    