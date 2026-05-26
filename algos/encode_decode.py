from typing import List

class Solution:

    def encode(self, strs: List[str]) -> str:
        s=[]

        for word in strs:
            x =len(word)
            s.append(f"{x}#{word}")
        return "".join(s)


    def decode(self, s: str) -> List[str]:

        finale = []
        a = 0

        while a < len(s):
            b = a
            # scan forward to find '#'
            while s[b] != '#':
                b = s.index('#', a)                
                numero = int(s[a:b])           # length number sits between a and '#'
                parola = s[b+1 : b+1+numero]   # word starts right after '#'
                finale.append(parola)
                a = b + 1 + numero             # advance past this word

        return finale


sol = Solution()
print(sol.decode(sol.encode(strs=["we","say",":","yes","!@#$%^&*()"])))

