fruits = ['peach', 'kiwi', 'apple', 'blueberry', 'papaya', 'mango', 'pear']

new_order = sorted(fruits, key=lambda fruit_name: (len(fruit_name), fruit_name))
for fruit in new_order:
    tuples = (len(fruit), fruit)  # Calculate the tuple
    print(f" {tuples}")
