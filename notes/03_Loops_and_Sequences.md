# Loops & Sequences , The Beginner-Friendly Guide

> Lists, tuples, loops, and the handy tools that make repetitive tasks effortless.

---

## Table of Contents

1. [Python Lists](#-python-lists)
2. [List Methods](#-list-methods)
3. [Tuples](#-tuples)
4. [Common Tuple Methods](#-common-tuple-methods)
5. [Loops in Python](#-loops-in-python)
6. [break, continue & loop-else](#-break-continue--loop-else)
7. [The range() Function](#-the-range-function)
8. [enumerate() & zip()](#-enumerate--zip)
9. [List Comprehensions](#-list-comprehensions)
10. [filter(), map() & sum()](#-filter-map--sum)
11. [Lambda Functions](#-lambda-functions)

---

## Python Lists

**Simple definition:** A list is an ordered, changeable collection of items , you can hold strings, numbers, or even other lists inside one.

**Analogy:** A list is like a numbered shopping list on your fridge , items are in a specific order, you can cross one out, add a new one, or swap an item for another, any time you like.

```python
cities = ['Los Angeles', 'London', 'Tokyo']

print(cities[0])   # Los Angeles → first item (indexing starts at 0)
print(cities[-1])  # Tokyo       → last item (negative index counts from the end)
```

### Building Lists from Other Things
```python
developer = 'Jessica'
print(list(developer))
# ['J', 'e', 's', 's', 'i', 'c', 'a']  → list() turns any iterable into a list
```

### Length, Updating & Deleting
```python
numbers = [1, 2, 3, 4, 5]
print(len(numbers))  # 5

# Lists are mutable , you can overwrite an item by its index
programming_languages = ['Python', 'Java', 'C++', 'Rust']
programming_languages[0] = 'JavaScript'
print(programming_languages)  # ['JavaScript', 'Java', 'C++', 'Rust']

# del removes an item completely
developer = ['Jane Doe', 23, 'Python Developer']
del developer[1]
print(developer)  # ['Jane Doe', 'Python Developer']
```

> Using an index that doesn't exist raises an `IndexError` , Python has no "slot 10" if your list only has 4 items.

### Checking Membership
```python
programming_languages = ['Python', 'Java', 'C++', 'Rust']
print('Rust' in programming_languages)        # True
print('JavaScript' in programming_languages)  # False
```

### Nested Lists
**Analogy:** A nested list is like a box inside a box , you open the outer box first, then reach into the inner one.

```python
developer = ['Alice', 25, ['Python', 'Rust', 'C++']]

print(developer[2])     # ['Python', 'Rust', 'C++'] → the nested list
print(developer[2][1])  # Rust → the 2nd item inside that nested list
```

### Unpacking Values
**Analogy:** Unpacking is like handing out party favors from a goodie bag , each variable grabs exactly one item, in order.

```python
developer = ['Alice', 34, 'Rust Developer']
name, age, job = developer
# name = 'Alice', age = 34, job = 'Rust Developer'

# Use * to scoop up "everything else" into one variable
name, *rest = developer
# name = 'Alice', rest = [34, 'Rust Developer']
```

> If your variable count doesn't match the list length (and you're not using `*`), you'll get a `ValueError`.

### Slicing Lists
```python
desserts = ['Cake', 'Cookies', 'Ice Cream', 'Pie']
print(desserts[1:3])   # ['Cookies', 'Ice Cream'] → index 1 up to (not including) 3

numbers = [1, 2, 3, 4, 5, 6]
print(numbers[1::2])   # [2, 4, 6] → start at index 1, step by 2
```

---

## List Methods

| Method | What it does | Example |
|---|---|---|
| `.append(x)` | Adds one item to the end | `[1,2].append(3)` → `[1,2,3]` |
| `.extend(list)` | Adds *multiple* items to the end | `[1,2].extend([3,4])` → `[1,2,3,4]` |
| `.insert(i, x)` | Inserts an item at a specific index | `[1,2].insert(1, 1.5)` → `[1,1.5,2]` |
| `.remove(x)` | Removes the *first* matching item | `[1,5,5].remove(5)` → `[1,5]` |
| `.pop(i)` | Removes and **returns** an item (last item if no index) | `[1,2,3].pop()` → returns `3` |
| `.clear()` | Empties the list completely | `[1,2].clear()` → `[]` |
| `.sort()` | Sorts the list **in place** | `[3,1,2].sort()` → `[1,2,3]` |
| `.reverse()` | Reverses the list in place | `[1,2,3].reverse()` → `[3,2,1]` |
| `.index(x)` | Finds the first index of an item | `['a','b'].index('b')` → `1` |

```python
# append() vs extend() , a common beginner trip-up!
numbers = [1, 2, 3, 4, 5]
even_numbers = [6, 8, 10]

numbers.append(even_numbers)
print(numbers)  # [1, 2, 3, 4, 5, [6, 8, 10]] adds the WHOLE list as one item

numbers = [1, 2, 3, 4, 5]
numbers.extend(even_numbers)
print(numbers)  # [1, 2, 3, 4, 5, 6, 8, 10] adds each item individually
```

> **`sort()` vs `sorted()`:** `sort()` changes the original list and returns nothing. `sorted()` leaves the original untouched and hands you a brand-new sorted list , use whichever fits your situation.

```python
numbers = [19, 2, 35, 1, 67, 41]
sorted_numbers = sorted(numbers)

print(sorted_numbers)  # [1, 2, 19, 35, 41, 67] → new list
print(numbers)          # [19, 2, 35, 1, 67, 41] → original is untouched
```

---

## Tuples

**Simple definition:** A tuple is like a list, but **locked** , once created, its contents can't be changed.

**Analogy:** A tuple is like a sealed jar of preserved fruit , you can look at what's inside and count it, but you can't add, remove, or swap anything without breaking the seal entirely.

```python
developer = ('Alice', 34, 'Rust Developer')

print(developer[1])  # 34 → access works just like a list
```

```python
# Trying to change a tuple raises a TypeError
programming_languages = ('Python', 'Java', 'C++', 'Rust')
programming_languages[0] = 'JavaScript'

"""
TypeError: 'tuple' object does not support item assignment
"""
```

### Other Tuple Basics
```python
numbers = (1, 2, 3, 4, 5)
print(numbers[-2])  # 4 → negative indexing works too

# Build a tuple from any iterable
developer = 'Jessica'
print(tuple(developer))  # ('J', 'e', 's', 's', 'i', 'c', 'a')

# Membership check
programming_languages = ('Python', 'Java', 'C++', 'Rust')
print('Rust' in programming_languages)  # True

# Unpacking works the same as lists
developer = ('Alice', 34, 'Rust Developer')
name, age, job = developer

# Slicing works the same too
desserts = ('cake', 'pie', 'cookies', 'ice cream')
print(desserts[1:3])  # ('pie', 'cookies')
```

> `del` on a tuple item raises a `TypeError` , tuples don't allow removal either.

### List vs Tuple , Which Do I Use?
- Need to **add, remove, or change** items later? → **List**
- Data is **fixed and shouldn't change** (like coordinates, or a date)? → **Tuple**

---

## Common Tuple Methods

Tuples only get two methods (since they're locked, there's less to do):

```python
programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust')

# count() , how many times does an item appear?
print(programming_languages.count('Rust'))       # 2
print(programming_languages.count('JavaScript'))  # 0

# index() , where's the first occurrence?
print(programming_languages.index('Java'))  # 1
```

> `index()` raises a `ValueError` if the item isn't found at all.

```python
# You can narrow the search with optional start/end positions
programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
print(programming_languages.index('Python', 3))  # 5 → search starting from index 3
```

### Sorting a Tuple
`sorted()` works on tuples too , but always hands back a **list**, not a tuple:

```python
numbers = (13, 2, 78, 3, 45, 67, 18, 7)
print(sorted(numbers))  # [2, 3, 7, 13, 18, 45, 67, 78]

# key= customizes what's sorted on (here, by word length)
programming_languages = ('Rust', 'Java', 'Python', 'C++', 'Rust', 'Python')
print(sorted(programming_languages, key=len))
# ['C++', 'Rust', 'Java', 'Rust', 'Python', 'Python']

# reverse=True flips the order
print(sorted(programming_languages, reverse=True))
# ['Rust', 'Rust', 'Python', 'Python', 'Java', 'C++']
```

---

## Loops in Python

**Simple definition:** A loop repeats a block of code, either a set number of times or until a condition changes.

**Analogy:** A loop is like a factory conveyor belt , the same action (the loop body) happens automatically to every item that comes down the line, without you doing it by hand each time.

### `for` Loop , "For each item, do this"
```python
programming_languages = ['Rust', 'Java', 'Python', 'C++']

for language in programming_languages:
    print(language)

# Rust
# Java
# Python
# C++
```

Loops work over strings too , each character is treated as an item:
```python
for char in 'code':
    print(char)
# c
# o
# d
# e
```

**Nested loops** , a loop inside a loop (analogy: like checking every combination on a restaurant menu , each starter paired with every main):
```python
categories = ['Fruit', 'Vegetable']
foods = ['Apple', 'Carrot', 'Banana']

for category in categories:
    for food in foods:
        print(category, food)

# Fruit Apple
# Fruit Carrot
# Fruit Banana
# Vegetable Apple
# Vegetable Carrot
# Vegetable Banana
```

### `while` Loop , "Keep going until this is False"
**Analogy:** A `while` loop is like knocking on a door repeatedly until someone answers , you don't know exactly how many knocks it'll take, just that you keep going until the condition (door opens) changes.

```python
secret_number = 3
guess = 0

while guess != secret_number:
    guess = int(input('Guess the number (1-5): '))
    if guess != secret_number:
        print('Wrong! Try again.')

print('You got it!')
```

---

## break, continue & loop-else

**Simple definition:**
- `break` = stop the loop entirely, right now
- `continue` = skip just this one round, then keep going

**Analogy:** Imagine checking mail in a row of mailboxes. `break` is like stopping the moment you find the letter you're looking for , no need to check the rest. `continue` is like skipping a mailbox that's empty, but still checking every other one after it.

```python
developer_names = ['Jess', 'Naomi', 'Tom']

# break , stops completely once 'Naomi' is hit
for developer in developer_names:
    if developer == 'Naomi':
        break
    print(developer)
# Jess

# continue , skips 'Naomi' but keeps checking the rest
for developer in developer_names:
    if developer == 'Naomi':
        continue
    print(developer)
# Jess
# Tom
```

### The `else` Clause on Loops
**Simple definition:** The `else` block after a loop only runs if the loop finished *without* hitting a `break`.

```python
words = ['sky', 'apple', 'rhythm', 'fly', 'orange']

for word in words:
    for letter in word:
        if letter.lower() in 'aeiou':
            print(f"'{word}' contains the vowel '{letter}'")
            break
    else:
        print(f"'{word}' has no vowels")  # only runs if no break happened
```

---

## The range() Function

**Simple definition:** `range()` generates a sequence of numbers , commonly used to control how many times a loop runs.

**Analogy:** `range()` is like setting a timer with a start point, an end point, and an interval , "count from 2 to 10, in steps of 2."

```python
range(start, stop, step)  # start & step are optional
```

```python
for num in range(3):
    print(num)
# 0
# 1
# 2   → stop (3) is never included!

for num in range(2, 11, 2):
    print(num)
# 2, 4, 6, 8, 10

for num in range(40, 0, -10):
    print(num)
# 40, 30, 20, 10   → negative step counts down
```

> `range()` only works with integers , passing a float raises a `TypeError`. And calling `range()` with no arguments raises one too.

**Turning a range into a list:**
```python
numbers = list(range(2, 11, 2))
print(numbers)  # [2, 4, 6, 8, 10]
```

---

## enumerate() & zip()

### enumerate() , "Give me the index AND the item"
**Analogy:** `enumerate()` is like numbering the runners in a race as they cross the finish line , you get both their position *and* who they are, together.

```python
languages = ['Spanish', 'English', 'Russian', 'Chinese']

for index, language in enumerate(languages):
    print(f'Index {index} and language {language}')

# Index 0 and language Spanish
# Index 1 and language English
# Index 2 and language Russian
# Index 3 and language Chinese
```

```python
# Works outside a loop too
print(list(enumerate(languages)))
# [(0, 'Spanish'), (1, 'English'), (2, 'Russian'), (3, 'Chinese')]
```

### zip() , "Pair up items from multiple lists"
**Analogy:** `zip()` is like a literal zipper on a jacket , it interlocks two separate rows of teeth (two lists) into one combined sequence, matching them up side by side.

```python
developers = ['Naomi', 'Dario', 'Jessica', 'Tom']
ids = [1, 2, 3, 4]

for name, id in zip(developers, ids):
    print(f'Name: {name}')
    print(f'ID: {id}')

# Name: Naomi   ID: 1
# Name: Dario   ID: 2
# Name: Jessica ID: 3
# Name: Tom     ID: 4
```

---

## List Comprehensions

**Simple definition:** A one-line shortcut for building a new list by looping and (optionally) filtering, all in a single readable expression.

**Analogy:** A list comprehension is like an assembly-line instruction card that says "for every item coming through, check this condition, then build a new item" , all summarized in one sentence instead of a whole paragraph of steps.

```python
# Longhand version:
even_numbers = []
for num in range(21):
    if num % 2 == 0:
        even_numbers.append(num)

# List comprehension , same result, one line:
even_numbers = [num for num in range(21) if num % 2 == 0]
print(even_numbers)  # [0, 2, 4, 6, ..., 20]
```

---

## filter(), map() & sum()

### filter() , "Keep only what passes the test"
**Analogy:** `filter()` is like a sieve , you pour everything in, and only the pieces that fit your criteria make it through.

```python
words = ['tree', 'sky', 'mountain', 'river', 'cloud', 'sun']

def is_long_word(word):
    return len(word) > 4

long_words = list(filter(is_long_word, words))
print(long_words)  # ['mountain', 'river', 'cloud']
```

### map() , "Transform every item"
**Analogy:** `map()` is like a factory stamping machine , the same transformation gets applied to every single item passing through.

```python
celsius = [0, 10, 20, 30, 40]

def to_fahrenheit(temp):
    return (temp * 9/5) + 32

fahrenheit = list(map(to_fahrenheit, celsius))
print(fahrenheit)  # [32.0, 50.0, 68.0, 86.0, 104.0]
```

### sum() , "Add it all up"
```python
numbers = [5, 10, 15, 20]
print(sum(numbers))  # 50

# Optional 'start' argument adds an initial value on top
print(sum(numbers, 10))         # 60 → positional
print(sum(numbers, start=10))   # 60 → keyword (same result, clearer intent)
```

---

## Lambda Functions

**Simple definition:** A lambda is a small, throwaway function written in a single line , it has no name of its own.

**Analogy:** A lambda function is like a sticky note with quick instructions, versus a fully bound instruction manual (a regular `def` function) , perfect for a quick, one-time job, not meant to be reused everywhere.

```python
numbers = [1, 2, 3, 4, 5]

# Regular function version:
def is_even(x):
    return x % 2 == 0
even_numbers = list(filter(is_even, numbers))

# Lambda version , same logic, no separate function needed:
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4]
```

> **Best practice:** Keep lambdas short and simple, use them for quick one-off jobs (often passed straight into `filter()`, `map()`, or `sorted()`), and avoid assigning them to a variable , if it needs a name, just write a regular function instead.

---

## Nice Work!

You've now got the full toolkit for handling collections of data , lists, tuples, loops, and the shortcuts (`enumerate`, `zip`, comprehensions, `filter`/`map`) that experienced Python developers reach for daily. These patterns show up constantly in real-world code, so the more you practice them, the more automatic they'll become.

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
