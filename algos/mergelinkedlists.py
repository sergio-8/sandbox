 # Definition for singly-linked list.


class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next
class Solution:
    def mergeTwoLists(self, list1: [ListNode], list2: [ListNode]) -> [ListNode]:
        
        

        x = list1
        y = list2
        dummy = ListNode()
        curr = dummy

        while x is not None and y is not None: 

            if x.val < y.val:
              
              curr.next = x
              curr =curr.next
              x = x.next

            elif x.val==y.val:

                curr.next = y
                curr = curr.next
                y = y.next

                curr.next = x
                curr= curr.next
                x = x.next
                
                  
                 
            else:
              curr.next = y
              curr= curr.next
              y=y.next

        if y is not None:
            curr.next = y

        if x is not None:
            curr.next = x

        return dummy.next


# Helper to build a linked list of many nodes
def build_list(vals):
    dummy = ListNode()
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next
# Helper to print a linked list so we can read it
def print_list(node):
    res = []
    while node is not None:
        res.append(node.val)
        node = node.next
    print(res)
# Create the lists properly
l1 = build_list([1, 2, 4])
l2 = build_list([1, 3, 4])
sol = Solution()
mergemarge = sol.mergeTwoLists(l1, l2)
# Print the result properly
print_list(mergemarge)