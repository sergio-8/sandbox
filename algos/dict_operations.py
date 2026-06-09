"""
=======================================================
  PYTHON DICTIONARY OPERATIONS — CHEAT SHEET
=======================================================
"""

# ─────────────────────────────────────────────────────
# 1. CREATING DICTIONARIES
# ─────────────────────────────────────────────────────

# Empty dict
empty = {}
also_empty = dict()

# With initial data
person = {"name": "Sergio", "age": 30, "city": "LA"}

# From a list of tuples
pairs = dict([("a", 1), ("b", 2), ("c", 3)])

# From keyword arguments
colors = dict(red="#FF0000", green="#00FF00", blue="#0000FF")

print("=== CREATING ===")
print(f"person:  {person}")
print(f"pairs:   {pairs}")
print(f"colors:  {colors}")


# ─────────────────────────────────────────────────────
# 2. WRITING / ASSIGNING (add or overwrite)
# ─────────────────────────────────────────────────────

print("\n=== WRITING / ASSIGNING ===")

# Add a new key
person["email"] = "sergio@email.com"
print(f"After adding email:  {person}")

# Overwrite an existing key
person["age"] = 31
print(f"After updating age:  {person}")

# Add multiple keys at once with update()
person.update({"phone": "555-1234", "job": "engineer"})
print(f"After update():      {person}")

# Merge with |= (Python 3.9+)
person |= {"hobby": "coding"}
print(f"After |= merge:      {person}")


# ─────────────────────────────────────────────────────
# 3. LOOKING UP / READING VALUES
# ─────────────────────────────────────────────────────

print("\n=== LOOKUP ===")

# Direct access — raises KeyError if key missing
print(f"person['name']:       {person['name']}")

# Safe access with .get() — returns None (or a default) if missing
print(f"person.get('name'):   {person.get('name')}")
print(f"person.get('salary'): {person.get('salary')}")           # None
print(f"person.get('salary', 0): {person.get('salary', 0)}")     # default = 0

# Check if a key exists
print(f"'name' in person:    {'name' in person}")      # True
print(f"'salary' in person:  {'salary' in person}")    # False


# ─────────────────────────────────────────────────────
# 4. LISTING KEYS, VALUES, AND PAIRS
# ─────────────────────────────────────────────────────

print("\n=== LISTING ===")

print(f"Keys:   {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"Pairs:  {list(person.items())}")

# Looping through a dict
print("\nLoop — keys only:")
for key in person:
    print(f"  {key}")

print("\nLoop — keys and values:")
for key, value in person.items():
    print(f"  {key} -> {value}")


# ─────────────────────────────────────────────────────
# 5. FINDING BY MATCHING KEY or VALUE
# ─────────────────────────────────────────────────────

print("\n=== SEARCHING ===")

scores = {"alice": 95, "bob": 82, "carol": 95, "dave": 70, "eve": 82}

# Find all keys with a specific value
target_score = 95
matching_keys = [k for k, v in scores.items() if v == target_score]
print(f"Who scored {target_score}? {matching_keys}")

# Find all keys containing a substring
people = {"alice_smith": 1, "bob_jones": 2, "alice_wong": 3}
alice_keys = [k for k in people if "alice" in k]
print(f"Keys with 'alice': {alice_keys}")

# Find all values above a threshold
high_scores = {k: v for k, v in scores.items() if v > 80}
print(f"Scores above 80:   {high_scores}")

# Find the key with the max value
top_student = max(scores, key=scores.get)
print(f"Top student:        {top_student} ({scores[top_student]})")


# ─────────────────────────────────────────────────────
# 6. REMOVING / DELETING
# ─────────────────────────────────────────────────────

print("\n=== REMOVING ===")

demo = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
print(f"Start:         {demo}")

# del — remove by key (raises KeyError if missing)
del demo["a"]
print(f"After del 'a': {demo}")

# pop() — remove by key and GET the value back (safe with default)
val = demo.pop("b")
print(f"After pop 'b': {demo}  (popped value: {val})")

val = demo.pop("zzz", "not found")  # safe — no KeyError
print(f"pop missing:   returned '{val}'")

# popitem() — remove the LAST inserted pair
last = demo.popitem()
print(f"After popitem: {demo}  (removed: {last})")

# clear() — remove everything
demo.clear()
print(f"After clear:   {demo}")


# ─────────────────────────────────────────────────────
# 7. SETDEFAULT — insert only if key is missing
# ─────────────────────────────────────────────────────

print("\n=== SETDEFAULT ===")

config = {"theme": "dark"}

# Key exists → does nothing, returns existing value
result = config.setdefault("theme", "light")
print(f"theme exists:     {config}  (returned: '{result}')")

# Key missing → inserts the default, returns it
result = config.setdefault("lang", "en")
print(f"lang was missing: {config}  (returned: '{result}')")


# ─────────────────────────────────────────────────────
# 8. MERGING TWO DICTIONARIES
# ─────────────────────────────────────────────────────

print("\n=== MERGING ===")

defaults = {"theme": "light", "font": "Arial", "size": 12}
user_prefs = {"theme": "dark", "size": 16}

# Method 1: unpack (Python 3.5+) — right side wins on conflicts
merged = {**defaults, **user_prefs}
print(f"Unpack merge:  {merged}")

# Method 2: | operator (Python 3.9+) — right side wins
merged2 = defaults | user_prefs
print(f"Pipe merge:    {merged2}")


# ─────────────────────────────────────────────────────
# 9. DICTIONARY COMPREHENSIONS
# ─────────────────────────────────────────────────────

print("\n=== COMPREHENSIONS ===")

# Create a dict from a range
squares = {x: x**2 for x in range(1, 6)}
print(f"Squares:       {squares}")

# Filter a dict
big_squares = {k: v for k, v in squares.items() if v > 9}
print(f"Squares > 9:   {big_squares}")

# Swap keys and values
flipped = {v: k for k, v in squares.items()}
print(f"Flipped:       {flipped}")


# ─────────────────────────────────────────────────────
# 10. USEFUL BUILT-INS
# ─────────────────────────────────────────────────────

print("\n=== USEFUL BUILT-INS ===")

d = {"x": 10, "y": 20, "z": 30}

print(f"Length:        {len(d)}")
print(f"Copy:          {d.copy()}")        # shallow copy
print(f"Sum of values: {sum(d.values())}")
print(f"Sorted keys:   {sorted(d)}")
print(f"Min value key:  {min(d, key=d.get)}")
print(f"Max value key:  {max(d, key=d.get)}")


# ─────────────────────────────────────────────────────
# 11. NESTED DICTIONARIES
# ─────────────────────────────────────────────────────

print("\n=== NESTED ===")

users = {
    "u1": {"name": "Alice", "scores": [90, 85, 92]},
    "u2": {"name": "Bob",   "scores": [78, 88, 95]},
}

# Access nested values
print(f"Alice's first score: {users['u1']['scores'][0]}")

# Add to nested dict
users["u1"]["email"] = "alice@mail.com"
print(f"After nested add:    {users['u1']}")
