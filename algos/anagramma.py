class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        
        a = sorted(s)
        b = sorted(t)

        if a==b:
            return True
        else:
            return False


test=Solution()

print(test.isAnagram("rat", "car")) #Expected result: False
print(test.isAnagram("anagram", "nagaram")) #Expected result: True
print(test.isAnagram("aab", "baa")) #Expected result: True
print(test.isAnagram("racecar", "carrace")) #Expected result: True
