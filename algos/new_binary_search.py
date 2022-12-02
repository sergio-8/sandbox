def binSearch(lst, elt):
    n = len(lst)
    if (elt < lst[0] or elt > lst[n-1]):
        return None
    else:
        left = 0
        right = n - 1
        while (left <= right):
            # Exact same logic as the recursion.
            mid = (left + right)//2
            if lst[mid] == elt:
                return (print(f"found ceppo in position {mid} ")) # found it.
            elif lst[mid] < elt:
                left = mid + 1
            else: # lst[mid] > elt
                right = mid - 1
        return None
