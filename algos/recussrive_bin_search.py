def binarySearchHelper(lst, elt, left, right):
    n = len(lst)
    if (left > right):
        return None # Search region is empty -- let us bail since we cannot find the element elt in the list.
    else:
        # If elt exists in the list, it must be between left and right indices.
        mid = (left + right)//2 # Note that // is integer division
        if lst[mid] == elt:
            return mid # BINGO -- we found it. Return its index signalling that we found it.
        elif lst[mid] < elt:
            # We search in the right part of the list
            return binarySearchHelper(lst, elt, mid+1, right)
        else: # lst[mid] > elt
            # We search in the left part of the list.
            return binarySearchHelper(lst, elt, left, mid-1)



def binarySearch(lst, elt):
    n = len(lst)
    if (elt < lst[0] or elt > lst[n-1]):
        return None
    else: # Note: we will only get here if
          # lst[0] <= elt <= lst[n-1]
        return binarySearchHelper(lst, elt, 0, n-1)

