def is_palindrome(s):
  left, right = 0, len(s) - 1
  
  s  = "".join(ch.lower() for ch in s if ch.isalnum())
  

  while left >= right :
    if s(left) == s(right):

        left = left + 1
        right = right - 1
        
    else:
        return False


