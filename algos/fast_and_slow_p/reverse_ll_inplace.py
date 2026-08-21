from importlib import _bootstrap_external
from decimal import DivisionImpossible
class Node:
    """A node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """The linked list manager."""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Adds a new node to the end of the list."""
        new_node = Node(data)
        
        # If the list is empty, make the new node the head
        if not self.head:
            self.head = new_node
            return
            
        # Otherwise, traverse to the last node and add the new node
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
            
        last_node.next = new_node

    def display(self):
        """Prints the linked list visually."""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")

# --- Creating the requested list ---

# Initialize the linked list
alphabet_list = LinkedList()

# The first 10 letters of the alphabet
first_10_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Populate the list
for letter in first_10_letters:
    alphabet_list.append(letter)

# Display the final list
alphabet_list.display()





#print (ora.data, prima , dopo.data)

def rigira(head):

    ora = head
    prima = None
    dopo = ora.next 

    while ora is not None:

        memoria = ora.next

        ora.next = prima

        prima = ora 

        ora = memoria

    new_list = LinkedList()
    new_list.head = prima
    return new_list

c = rigira (alphabet_list.head)
c.display()