class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def get_middle_node(head):

    # Replace this placeholder return statement with your code
    
    slow = head
    fast = head
    count = 0
    
    while fast.next and fast is not None:
        s = slow.next
        f = fast.next.next
        count = count+1
        
        slow = s 
        fast = f
        continue
        
    
    #if count % 2 == 0:
    #    return slow.next
    
    return slow
   


# Create the nodes
node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)
# Connect them: 1 -> 2 -> 3 -> 4 -> 5
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
# Call function and print the value of the middle node
middle = get_middle_node(node1)
print(middle.val if middle else "None")
