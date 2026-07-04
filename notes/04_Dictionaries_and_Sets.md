# Dictionaries & Sets , The Beginner-Friendly Guide

> Key-value storage, unique collections, and how to borrow code from Python's own toolbox.

---

## Table of Contents

1. [Dictionaries](#-dictionaries)
2. [Common Dictionary Methods](#-common-dictionary-methods)
3. [Looping Over a Dictionary](#-looping-over-a-dictionary)
4. [Sets](#-sets)
5. [Common Set Methods](#-common-set-methods)
6. [Mathematical Set Operations](#-mathematical-set-operations)
7. [Python Standard Library](#-python-standard-library)
8. [Import Statements](#-import-statements)
9. [if \_\_name\_\_ == '\_\_main\_\_'](#-if-__name__--__main__)

---

## Dictionaries

**Simple definition:** A dictionary stores data as **key-value pairs** , instead of finding an item by its position (like a list), you find it by its label.

**Analogy:** A dictionary is like a real paper dictionary or a phone contacts app , you don't look up a friend's number by "the 47th entry," you look them up by their *name* (the key), and it hands you their number (the value).

```python
dictionary = {
    key1: value1,
    key2: value2
}
```

> Keys must be **immutable** (strings, numbers, tuples) , you can't use a list as a key, since it could change later and break the lookup.

### Creating Dictionaries Two Ways
```python
# Standard curly-brace syntax
pizza = {
    'name': 'Margherita Pizza',
    'price': 8.9
}

# Alternative: dict() constructor, built from a list of (key, value) tuples
pizza = dict([
    ('name', 'Margherita Pizza'),
    ('price', 8.9),
    ('calories_per_slice', 250),
    ('toppings', ['mozzarella', 'basil'])
])
```

### Accessing Values
```python
pizza = {'name': 'Margherita Pizza', 'price': 8.9}

print(pizza['name'])  # Margherita Pizza → bracket notation
```

---

## Common Dictionary Methods

### `.get()` , the safer way to look things up
**Simple definition:** Works like bracket notation, but lets you set a fallback value instead of crashing if the key doesn't exist.

**Analogy:** It's like asking a librarian for a book , if `pizza['crust']` is like demanding the book exist or the whole library shuts down, `.get('crust', 'Not specified')` is like politely asking and being told "we don't have that, but here's a default answer" instead.

```python
pizza = {'name': 'Margherita Pizza', 'price': 8.9}

print(pizza.get('price', 0))    # 8.9  → key exists
print(pizza.get('crust', 'Not specified'))  # 'Not specified' → key missing, no crash
```

### `.keys()`, `.values()`, `.items()`
```python
pizza = {
    'name': 'Margherita Pizza',
    'price': 8.9,
    'calories_per_slice': 250
}

pizza.keys()    # dict_keys(['name', 'price', 'calories_per_slice'])
pizza.values()  # dict_values(['Margherita Pizza', 8.9, 250])
pizza.items()   # dict_items([('name', 'Margherita Pizza'), ('price', 8.9), ('calories_per_slice', 250)])
```

> These return "view objects" , think of them as a live window into the dictionary's current contents, rather than a separate copy.

### Removing & Updating Items

| Method | What it does | Example |
|---|---|---|
| `.clear()` | Wipes everything | `pizza.clear()` → `{}` |
| `.pop(key, default)` | Removes a key & **returns its value** | `pizza.pop('price', 10)` |
| `.popitem()` | Removes the **most recently added** item | `pizza.popitem()` |
| `.update({...})` | Merges in new/updated key-value pairs | `pizza.update({'price': 15})` |

```python
pizza = {'name': 'Margherita Pizza', 'price': 8.9}

pizza.pop('price', 10)      # removes 'price', returns 8.9
pizza.pop('total_price')    # KeyError , key doesn't exist, and no default given

# update() overwrites shared keys and adds new ones
pizza.update({'price': 15, 'total_time': 25})
```

---

## Looping Over a Dictionary

**Analogy:** Looping over a dictionary is like flipping through a filing cabinet , you can choose to look at just the folder labels (keys), just the contents (values), or both together (items).

```python
products = {
    'Laptop': 990,
    'Smartphone': 600,
    'Tablet': 250,
    'Headphones': 70,
}

# Just the values
for price in products.values():
    print(price)
# 990, 600, 250, 70

# Just the keys , both of these work identically
for product in products.keys():
    print(product)

for product in products:  # dictionaries loop over keys by default
    print(product)
# Laptop, Smartphone, Tablet, Headphones

# Both key AND value together
for product, price in products.items():
    print(product, price)
# Laptop 990
# Smartphone 600
# Tablet 250
# Headphones 70
```

### Adding a Counter with enumerate()
```python
for index, product in enumerate(products.items()):
    print(index, product)
# 0 ('Laptop', 990)
# 1 ('Smartphone', 600)
# 2 ('Tablet', 250)
# 3 ('Headphones', 70)

# Start counting from a custom number
for index, product in enumerate(products.items(), 1):
    print(index, product)
# 1 ('Laptop', 990)
# 2 ('Smartphone', 600)
# 3 ('Tablet', 250)
# 4 ('Headphones', 70)
```

---

## Sets

**Simple definition:** A set is an unordered collection that automatically removes duplicates , every item in it is guaranteed unique.

**Analogy:** A set is like a guest list at a private event , no matter how many times someone tries to RSVP twice, they only appear on the list once. And since it's just a list of names (not seats), there's no "1st guest, 2nd guest" order to rely on.

```python
my_set = {1, 2, 3, 4, 5}
```

> Sets can only hold **immutable** items (numbers, strings, tuples) , no lists or dictionaries inside a set.

### Creating an Empty Set
```python
empty_set = set()   # this is a set
empty_dict = {}      # this is actually a DICTIONARY, not a set!
```

---

## Common Set Methods

| Method | What it does | Example |
|---|---|---|
| `.add(x)` | Adds an item | `my_set.add(6)` |
| `.remove(x)` | Removes an item , **raises `KeyError`** if missing | `my_set.remove(4)` |
| `.discard(x)` | Removes an item , **stays silent** if missing | `my_set.discard(4)` |
| `.clear()` | Empties the set | `my_set.clear()` |

> **`remove()` vs `discard()`:** Use `discard()` when you're not sure the item exists and don't want your program to crash over it.

---

## Mathematical Set Operations

**Analogy:** Think of two overlapping circles in a Venn diagram , these operators let you grab exactly the slice you need (just the overlap, everything combined, or everything except the overlap).

```python
my_set = {1, 2, 3, 4, 5}
your_set = {2, 3, 4, 6}
```

| Operator/Method | Meaning | Result |
|---|---|---|
| `\|` (union) | Everything from both sets | `my_set \| your_set` → `{1,2,3,4,5,6}` |
| `&` (intersection) | Only what's shared | `my_set & your_set` → `{2,3,4}` |
| `-` (difference) | In the first set, but not the second | `my_set - your_set` → `{1,5}` |
| `^` (symmetric difference) | In either set, but **not** both | `my_set ^ your_set` → `{1,5,6}` |

```python
# Subset / superset checks
my_set = {1, 2, 3, 4, 5}
your_set = {2, 3, 4, 5}

print(your_set.issubset(my_set))    # True → is every item in your_set also in my_set?
print(my_set.issuperset(your_set))  # True → does my_set contain everything in your_set?

# isdisjoint() , do the sets have ZERO items in common?
set_a = {1, 2, 3}
set_b = {4, 5, 6}
print(set_a.isdisjoint(set_b))  # True

# Membership check
print(5 in my_set)  # True
```

---

## Python Standard Library

**Simple definition:** A huge collection of pre-written, ready-to-use code (functions, classes, tools) that ships with Python , no extra installation needed.

**Analogy:** The Standard Library is like a fully-stocked toolbox that comes free with every house you move into , you don't need to buy a hammer; it's already in the drawer, waiting for you to use it.

Popular built-in modules include:
- `math` , mathematical operations
- `random` , generating random values
- `re` , regular expressions (pattern matching in text)
- `datetime` , working with dates and times

---

## Import Statements

**Simple definition:** An `import` statement lets you pull in code from a module so you can use it in your own script.

**Analogy:** Importing a module is like borrowing a specific toolset from a shared workshop , you say what you need, and it becomes available on your own workbench.

### Basic Import
```python
import math

print(math.sqrt(36))  # 6.0 → access with dot notation: module.function()
```

### Import with an Alias
**Analogy:** Like giving a long name a nickname , easier to reference every time you need it.

```python
import math as m

print(m.sqrt(36))  # 6.0
```

### Importing Specific Elements
```python
from math import radians, sin, cos

angle_degrees = 40
angle_radians = radians(angle_degrees)

print(sin(angle_radians))  # 0.6427876096865393
print(cos(angle_radians))  # 0.766044443118978
```

> This can cause naming conflicts if you already have a variable or function with the same name , use it thoughtfully.

You can also alias specific imports:
```python
from math import radians as rad, sin as s
```

### Import Everything with `*`
```python
from math import *

print(sqrt(36))  # 6.0 → no "math." prefix needed
```

> **Generally discouraged** , it's hard to tell where a function came from, and it risks silently overwriting names you already have.

---

## if \_\_name\_\_ == '\_\_main\_\_'

**Simple definition:** `__name__` is a special variable Python sets automatically. It equals `"__main__"` when a file is run directly, but equals the module's name when that file is *imported* into another script.

**Analogy:** Think of it like a stage performer checking "am I the headline act tonight, or am I just a guest appearing in someone else's show?" The code inside this `if` block only runs when the file is the headline act (run directly) , not when it's imported as a supporting module elsewhere.

```python
if __name__ == '__main__':
    # This code only runs when this file is executed directly ,
    # not when it's imported into another script.
    print("Running as the main program!")
```

This pattern is everywhere in real Python projects , it's how a file can be *both* a standalone script *and* a reusable module, depending on how it's used.

---

## Well Done!

You've now got two more powerful data structures in your toolkit , dictionaries for labeled data, and sets for guaranteed-unique collections , plus the mechanics of borrowing code via imports. These show up constantly in real projects, from config files to data processing pipelines. Keep building! 

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
