def detect_cycle(head):
   
   if head is None or head.next is None:
    return False

   fast = head.next
   slow = head
   
   while fast is not None and fast.next is not None:
      
      if fast == slow:
         return True
      
      slow = slow.next
      fast = fast.next.next
         

   return False