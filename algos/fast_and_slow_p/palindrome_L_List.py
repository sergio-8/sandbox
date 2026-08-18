# Definition for a Linked List node
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
#from ds_v1.LinkedList.LinkedList import ListNode
#from LinkedListReversal import reverse_linked_list

def palindrome(head):
    
    lento = head
    veloce = head
    rebase = head
    
    while veloce.next is not None and veloce.next.next is not None:
        l = lento.next
        v = veloce.next.next
        lento = l
        veloce = v
        continue
    
    
    prev = None
    corrente = lento.next


    while corrente is not None :  
        
        next_temp = corrente.next

        corrente.next = prev

        prev = corrente

        corrente = next_temp
        
    restart = prev
    while prev is not None :

        if rebase.val == prev.val:

            rebase = rebase.next
            prev = prev.next
        else:
            return False

    
    return True
    
    
    
    
    

    # Replace this placeholder return statement with your code
    return False

def build_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

head = build_linked_list([4, 7, 9, 5, 4])
print(palindrome(head))