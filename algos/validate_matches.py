

class Solution:
    def isValid(self, s: str) -> bool:
        
        openers= ["(", "[", "{"]
        closers= [")","]", "}" ]
        opener = {"(", "[", "{"}

        stack = []
        match = dict(zip(closers, openers))
        
        
        for item in s:
            if item in opener:
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