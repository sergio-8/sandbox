

class Solution:
    def isValid(self, s: str) -> bool:
        
        openers= ["(", "[", "{"]
        closers= [")","]", "}" ]

        stack = []
        match = dict(zip(closers, openers))
        
        
        for item in s:
            if item in openers:
                stack.append(item)

            elif item in closers:
                if not stack or stack[-1] != match[item]:
                    return False
                stack.pop()

        return len(stack)==0     


sol = Solution()
print(sol.isValid("()[]{}")) 
print(sol.isValid("(]")) 
print(sol.isValid("{[]}")) 
print(sol.isValid(s="([{}])"))