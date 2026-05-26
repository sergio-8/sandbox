class Solution:
    def isPalindrome(self, s: str) -> bool:
        dir = []
        indir = []
        #s_low=s.lower()

        for char in s.replace(" ","").lower() :
            if char.isalnum():
                dir.append(char)
                indir.append(char)
        indir.reverse()
        if dir == indir:
            return True
        else:
            return False



sol=Solution()
print(sol.isPalindrome("A man, a plan, a canal: Panama"))
print(sol.isPalindrome("Was it a car or a cat I saw?"))
print(sol.isPalindrome("race a car"))
print(sol.isPalindrome("Was it a car or a cat I saw?"))