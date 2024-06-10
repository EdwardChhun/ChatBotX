query = "I want you to pick up a bottle from the table"

# Partition the string at "pick up"
before, sep, after = query.partition("pick up")

# If the separator is found, 'after' will contain the desired part
if sep:  # sep is "pick up" if found, empty otherwise
    item = after.strip()  # Strip leading/trailing spaces
else:
    item = None  # If "pick up" is not found

print("Item:", item)  # Output: "a bottle"
