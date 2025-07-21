---
layout: default
title: "Set Theory and Truth Table Exercises"
---

# Set Theory and Truth Table Exercises

## Set Theory Exercises in Python

### Exercise 1: Basic Set Operations

```python
# Define some sets
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}
C = {2, 4, 6, 8, 10}

# Union (A ∪ B)
union_AB = A.union(B)
print(f"A ∪ B = {union_AB}")

# Intersection (A ∩ B)
intersection_AB = A.intersection(B)
print(f"A ∩ B = {intersection_AB}")

# Difference (A - B)
difference_AB = A.difference(B)
print(f"A - B = {difference_AB}")

# Symmetric difference (A Δ B)
sym_diff_AB = A.symmetric_difference(B)
print(f"A Δ B = {sym_diff_AB}")

# Subset check
print(f"Is {{4, 5}} ⊆ A? {set([4, 5]).issubset(A)}")
```

Output:
```
A ∪ B = {1, 2, 3, 4, 5, 6, 7, 8}
A ∩ B = {4, 5}
A - B = {1, 2, 3}
A Δ B = {1, 2, 3, 6, 7, 8}
Is {4, 5} ⊆ A? True
```

### Exercise 2: Set Relationships and Logic

```python
# Knowledge representation using sets
animals = {"cat", "dog", "bird", "fish"}
mammals = {"cat", "dog", "whale", "bat"}
pets = {"cat", "dog", "bird", "hamster"}

# Which animals are both mammals and pets?
mammal_pets = mammals.intersection(pets)
print(f"Mammal pets: {mammal_pets}")

# Which pets are not mammals?
non_mammal_pets = pets.difference(mammals)
print(f"Non-mammal pets: {non_mammal_pets}")

# Are all pets animals? (subset check)
all_pets_are_animals = pets.issubset(animals)
print(f"All pets are animals: {all_pets_are_animals}")
```

Output:
```
Mammal pets: {'cat', 'dog'}
Non-mammal pets: {'bird', 'hamster'}
All pets are animals: False
```

## Truth Table Exercise

### Boolean Logic Mapping to Set Operations

| Set Operation | Boolean Logic | Truth Table |
|---------------|---------------|-------------|
| A ∪ B         | A OR B        | T when either A or B is true |
| A ∩ B         | A AND B       | T when both A and B are true |
| A'            | NOT A         | T when A is false |

### Example Truth Table: (A ∩ B) ∪ C

```python
def truth_table_example(A, B, C):
    """Demonstrate (A ∩ B) ∪ C using sets and boolean logic"""
    
    # Set representation
    result_set = (A.intersection(B)).union(C)
    
    # Boolean logic equivalent
    # For each element in universal set, check if it satisfies the condition
    universal = A.union(B).union(C)
    result_bool = set()
    
    for x in universal:
        if (x in A and x in B) or (x in C):
            result_bool.add(x)
    
    print(f"Set result: {result_set}")
    print(f"Boolean result: {result_bool}")
    print(f"Results match: {result_set == result_bool}")

# Test the function
A = {1, 2, 3}
B = {2, 3, 4}
C = {3, 4, 5}

truth_table_example(A, B, C)
```

Output:
```
Set result: {2, 3, 4, 5}
Boolean result: {2, 3, 4, 5}
Results match: True
```

## Key Insights

1. **Set operations directly map to logical operations** - Union is OR, Intersection is AND
2. **Truth tables help visualize** when logical expressions are true or false
3. **Python sets make it easy** to experiment with these concepts
4. **Knowledge representation often uses** these fundamental operations to define relationships

---

[← Back to Unit 2](/krr/#unit-2) | [KRR Module Home](/krr/)