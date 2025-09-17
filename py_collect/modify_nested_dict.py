nested2 = [{'a': 1, 'b': 3}, {'a': 5, 'c': 90, 5: 50}, {'b': 3, 'c': "yes"}]

# Print the original value
print(f"Original value of 'c' in third dictionary: {nested2[2]['c']}")

# Change the value associated with 'c' in the third dictionary from "yes" to "no"
nested2[2]['c'] = "no"

# Print to check our work
print(f"New value of 'c' in third dictionary: {nested2[2]['c']}")
print(f"Complete third dictionary: {nested2[2]}")
print(f"Complete nested2 list: {nested2}")