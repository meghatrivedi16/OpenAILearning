# Example set
my_set = {10, 20, 30, 40, 50, 50, 40}
another_set = {30, 40, 50, 60, 70}
yet_another_set = {100, 200}

# Displaying the set (properties)
print("Original set:", my_set)

# 1. Basic Operations
my_set.add(60)  # Add an element
print("After adding 60:", my_set)

my_set.remove(20)  # Remove an element
print("After removing 20:", my_set)

my_set.discard(100)  # Discard an element (does not raise an error if not found)
print("After discarding 100:", my_set)

popped_element = my_set.pop()  # Remove and return a random element
print("Popped element:", popped_element)
print("After popping an element:", my_set)

my_set.clear()  # Clear the set
print("After clearing the set:", my_set)
# Reinitialize the set for further examples
my_set = {10, 20, 30, 40, 50}

my_set.update(another_set)  # Update the set with another set
print("After updating my_set with another_set:", my_set)

# Length and Membership Testing
my_set = {10, 20, 30, 40, 50}
print("Length of my_set:", len(my_set))  # Length of the set
print("Is 20 in my_set?", 20 in my_set)  # Membership testing
print("Is 100 not in my_set?", 100 not in my_set)  # Membership testing