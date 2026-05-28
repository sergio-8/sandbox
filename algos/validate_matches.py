

class Solution:

    openers= ["(", "[", "{"]
    closers= [")","]", "}" ]
    opener = {"(", "[", "{"}
    
    def isValid(self, s: str) -> bool:
        
        if len(s)%2!=0:
            return False


        stack = []
        match = dict(zip(self.closers, self.openers))
        
        
        for item in s:
            if item in self.opener:
                stack.append(item)

            elif item in match:
                if not stack or stack[-1] != match[item]:
                    return False
                stack.pop()

        return len(stack)==0  

sol = Solution()
print(sol.isValid("()[]{}")) 
print(sol.isValid("(]")) 
print(sol.isValid("{[]}")) 
print(sol.isValid(s="([{}])"))
print(sol.isValid(s="([{}]))"))