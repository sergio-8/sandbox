"""
=======================================================
  PYTHON DICTIONARY OPERATIONS — QUIZ
=======================================================
Instructions: Fill in the code below each comment to complete the tasks.
You can run this file to check your work!
"""

print("=== Q1: CREATION ===")
# 1. Create an empty dictionary called 'inventory'
# TODO: Write your code here
inventory = dict()

print(f"1. inventory: {inventory} (Expected: {{}})")


print("\n=== Q2: ASSIGNMENT ===")
# 2. Add an item to 'inventory' where the key is "apples" and the value is 10
# TODO: Write your code here
inventory["apples"] = 10


print(f"2. inventory: {inventory} (Expected: {{'apples': 10}})")


print("\n=== Q3: OVERWRITE ===")
# 3. Update the value of "apples" to be 15
# TODO: Write your code here
inventory['apples'] = 15


print(f"3. inventory: {inventory} (Expected: {{'apples': 15}})")


print("\n=== Q4: BULK ADD ===")
# 4. Add two new items at once: "bananas" (5) and "oranges" (20)
# (Hint: use the .update() method or |= operator)
# TODO: Write your code here
inventory.update(bananas = 5,  oranges =20)



print(f"4. inventory: {inventory} (Expected: {{'apples': 15, 'bananas': 5, 'oranges': 20}})")


print("\n=== Q5: SAFE LOOKUP ===")
# 5. Get the value of "pears" safely so that it returns 0 if it doesn't exist, and store it in a variable 'pears_count'
# TODO: Write your code here
pears_count = ...

print(f"5. pears_count: {pears_count} (Expected: 0)")


print("\n=== Q6: CHECK EXISTENCE ===")
# 6. Check if "bananas" is a key in the inventory, store the boolean result in 'has_bananas'
# TODO: Write your code here
has_bananas = ...

print(f"6. has_bananas: {has_bananas} (Expected: True)")


print("\n=== Q7: LOOPING ===")
# 7. Write a loop that prints out each key and value in the format "We have [value] [key]."
# (Hint: use .items())
print("7. Loop output:")
# TODO: Write your code here



print("\n=== Q8: REMOVAL ===")
# 8. Remove "apples" from the inventory
# TODO: Write your code here


print(f"8. inventory: {inventory} (Expected: {{'bananas': 5, 'oranges': 20}})")

print("\n--- End of Quiz ---")
