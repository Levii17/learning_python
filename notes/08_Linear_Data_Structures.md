# Linear Data Structures — The Beginner-Friendly Guide

> Algorithms, Big O notation, and the core data structures that power efficient code — arrays, stacks, queues, linked lists, hash maps, and sets.

---

## Table of Contents

1. [Algorithms & Big O Notation](#-algorithms--big-o-notation)
2. [Common Time Complexities](#-common-time-complexities)
3. [Space Complexity](#-space-complexity)
4. [Problem-Solving Techniques](#-problem-solving-techniques)
5. [Arrays](#-arrays)
6. [Stacks](#-stacks)
7. [Queues](#-queues)
8. [Linked Lists](#-linked-lists)
9. [Hash Maps](#-hash-maps)
10. [Sets](#-sets)
11. [Hash Collisions](#-hash-collisions)
12. [When to Use Each Data Structure](#-when-to-use-each-data-structure)

---

## Algorithms & Big O Notation

**Simple definition:** An algorithm is a precise, step-by-step set of instructions for solving a problem — it must always finish, and every step must be crystal clear.

**Analogy:** An algorithm is like a recipe — vague instructions like "cook until it feels right" don't count; a real recipe has clear, ordered, unambiguous steps that reliably produce the same dish every time.

**Big O Notation** describes how an algorithm's performance (time or memory) grows as the input size grows — specifically, its *worst-case* behavior.

**Analogy:** Think of Big O like describing how long a queue takes to clear, not based on today's lucky short line, but based on the worst possible rush-hour crowd. It's less about exact seconds and more about the *pattern* of how wait times scale as more people join.

---

## Common Time Complexities

| Complexity | Name | What it means |
|---|---|---|
| `O(1)` | Constant | Same speed no matter the input size |
| `O(log n)` | Logarithmic | Grows slowly — repeatedly cuts the problem down |
| `O(n)` | Linear | Grows directly proportional to input size |
| `O(n log n)` | Log-Linear | Common in efficient sorting algorithms |
| `O(n²)` | Quadratic | Grows by the square — common in nested loops |

**Analogy for the shape of the growth:** `O(1)` is like checking if a light switch is on — takes the same instant whether there's 1 room or 1,000 rooms in the house. `O(n²)` is like everyone at a party shaking hands with everyone else — the more people you add, the number of handshakes explodes far faster than the guest count itself.

```python
# O(1) — Constant Time: same speed regardless of input size
def check_even_or_odd(number):
    if number % 2 == 0:
        return 'Even'
    else:
        return 'Odd'
```

```python
# O(n) — Linear Time: one pass through the data
for grade in grades:
    print(grade)
```

```python
# O(n²) — Quadratic Time: a loop nested inside another loop
for i in range(n):
    for j in range(n):
        print("Hello, World!")
```

> `O(log n)` shows up in algorithms like **Binary Search**, which repeatedly cuts the remaining data in half instead of checking every item one by one.

---

## Space Complexity

**Simple definition:** Just like time complexity measures speed, space complexity measures how much **memory** an algorithm needs as input size grows.

| Complexity | Meaning |
|---|---|
| `O(1)` | Uses the same memory no matter the input size |
| `O(n)` | Memory usage grows in direct proportion to input |
| `O(n²)` | Memory usage grows by the square of the input |

---

## Problem-Solving Techniques

### Understanding the Problem
Before writing any code, read the problem statement more than once. Identify:
- What's the **input**?
- What's the expected **output**?
- What transformation turns one into the other?

### Pseudocode
**Simple definition:** A high-level, language-independent way to sketch out your algorithm's logic using plain English mixed with programming-style structure (`IF`, `ELSE`, `FOR`, `WHILE`).

**Analogy:** Pseudocode is like a rough sketch before painting — you're mapping out the composition without worrying about exact brushstrokes (syntax) yet.

```
GET original_string
SET reversed_string = ""
FOR EACH character IN original_string:
  ADD character TO THE BEGINNING OF reversed_string
DISPLAY reversed_string
```

### Edge Cases
**Simple definition:** Edge cases are the unusual, boundary-level inputs your algorithm needs to handle correctly — empty inputs, single-item inputs, negative numbers, duplicates, and so on.

**Analogy:** Edge cases are like stress-testing a bridge not just with normal traffic, but with the heaviest truck, a single pedestrian, or zero cars at all — you want to know it holds up in every scenario, not just the average one.

---

## Arrays

**Simple definition:** An array is a collection of elements stored in order, usually right next to each other in memory.

**Analogy:** A static array is like a fixed row of numbered lockers — the count is set in stone the moment they're built. A dynamic array is like a row of lockers that can magically extend itself with more lockers whenever you run out of room.

- **Static Arrays:** Fixed size, set at creation — can't grow or shrink
- **Dynamic Arrays:** Automatically resize (usually by copying to a bigger array behind the scenes) as needed

### Python Lists Are Dynamic Arrays
```python
numbers = [3, 4, 5, 6]

numbers[0]           # 3        → access
numbers[2] = 16      # update
numbers.append(7)    # add to the end
numbers.insert(3, 15) # insert at a specific index
numbers.pop(2)       # remove at a specific index
numbers.pop()        # remove the last element
```

### Time Complexities for Dynamic Arrays

| Operation | Time Complexity |
|---|---|
| Access by index | `O(1)` |
| Insert at end | `O(1)` average, `O(n)` if resizing is triggered |
| Insert in middle | `O(n)` — everything after must shift |
| Delete | `O(1)` at the end, `O(n)` in the middle |

---

## Stacks

**Simple definition:** A stack follows **Last-In, First-Out (LIFO)** — the most recently added item is the first one removed.

**Analogy:** A stack is like a pile of plates on a counter — you can only add a new plate to the top, and you can only take a plate off from the top. You'd never yank one out from the bottom without the whole pile toppling.

```python
# Using a Python list as a stack
stack = []

# Push — adding to the top
stack.append(1)
stack.append(2)
stack.append(3)

# Pop — removing from the top
top_element = stack.pop()  # Returns 3
```

- **Push:** add to the top → `O(1)`
- **Pop:** remove from the top → `O(1)`

> Stacks power things like the "undo" button in editors, and how your browser remembers your "back" history.

---

## Queues

**Simple definition:** A queue follows **First-In, First-Out (FIFO)** — the first item added is the first one removed.

**Analogy:** A queue is exactly like a line at a coffee shop — whoever joined the line first gets served first, and new people join at the back, not the front.

```python
from collections import deque

queue = deque()

# Enqueue — adding to the back
queue.append(1)
queue.append(2)
queue.append(3)

# Dequeue — removing from the front
first_element = queue.popleft()  # Returns 1
```

- **Enqueue:** add to the back → `O(1)`
- **Dequeue:** remove from the front → `O(1)`

> Why `deque` instead of a plain list? Removing from the *front* of a regular Python list is slow (`O(n)`, since everything shifts down), but `deque` is built to make that operation just as fast as removing from the end.

---

## Linked Lists

**Simple definition:** A linked list is a chain of "nodes," where each node holds some data plus a reference (pointer) to the next node in the chain.

**Analogy:** A linked list is like a scavenger hunt — each clue (node) tells you the answer *and* where to find the next clue. You can't jump straight to clue #5; you have to follow the chain from the start.

### Singly Linked Lists
- Each node has data + **one** reference (to the next node)
- You can only move **forward**, from head to tail
- **Head:** the first node — usually the only one you can access directly
- **Tail:** the last node — its "next" reference points to `None`

| Operation | Time Complexity | Why |
|---|---|---|
| Insert at beginning | `O(1)` | Just attach a new head |
| Insert at end | `O(n)` | Must walk the whole chain to reach the end |
| Insert in middle | `O(n)` | Must walk to the right position |
| Delete from beginning | `O(1)` | Just detach the head |
| Delete from end | `O(n)` | Must find the node just before it |
| Delete from middle | `O(n)` | Must locate the target node first |

### Doubly Linked Lists
**Analogy:** A doubly linked list is like that same scavenger hunt, but each clue *also* tells you how to get back to the previous clue — you can now walk the trail in either direction, at the cost of carrying one extra piece of information at each stop.

- Each node has data + **two** references (next *and* previous)
- Can traverse in **both directions**
- Uses more memory than a singly linked list, due to that extra reference

---

## Hash Maps

**Simple definition:** A hash map (Python's dictionary) stores key-value pairs, using a **hash function** to quickly figure out exactly where to store and retrieve each key.

**Analogy:** A hash map is like a library that assigns each book a very specific shelf number based on its title — instead of scanning every shelf, the hash function tells you instantly which shelf to walk straight to.

```python
my_dictionary = {"A": 1, "B": 2, "C": 3}

# Alternative creation
my_dictionary = dict(A=1, B=2, C=3)

value = my_dictionary["A"]   # 1     → access
my_dictionary["A"] = 4        # update
del my_dictionary["A"]        # remove

"C" in my_dictionary           # membership check

my_dictionary.keys()
my_dictionary.values()
my_dictionary.items()
```

### Time Complexities for Hash Maps
- **Average case:** `O(1)` for insert, get, and delete
- **Worst case:** `O(n)` — happens when many hash collisions pile up

---

## Sets

**Simple definition:** A set is an unordered collection that only allows unique elements — no duplicates, no guaranteed order.

**Analogy:** A set is like a guest list where each name can only appear once, no matter how many times someone tries to sign up twice.

```python
numbers = {1, 2, 3, 4}
empty_set = set()  # must use set() — {} creates an empty dictionary instead!

numbers.add(5)
numbers.remove(4)   # raises KeyError if the item isn't found
numbers.discard(4)  # stays silent if the item isn't found

set_a = {1, 2, 3, 4}
set_b = {2, 3, 4, 5, 6}

set_a.union(set_b)                 # or set_a | set_b
set_a.intersection(set_b)          # or set_a & set_b
set_a.difference(set_b)            # or set_a - set_b
set_a.symmetric_difference(set_b)  # or set_a ^ set_b

set_a.issubset(set_b)
set_a.issuperset(set_b)
set_a.isdisjoint(set_b)

5 in numbers  # membership check
```

> Sets can only hold **immutable** items (numbers, strings, tuples) — this is because their hash value must never change once stored.

### Time Complexities for Sets
- **Average case:** `O(1)` for add, remove, and membership testing
- **Worst case:** `O(n)` due to hash collisions

---

## Hash Collisions

**Simple definition:** A hash collision happens when two different keys happen to produce the same hash value — meaning they'd otherwise want to occupy the same storage spot.

**Analogy:** Imagine two different people getting assigned the same locker number by accident — the system needs a backup plan for what happens next.

**Collision resolution strategies:**
- **Chaining:** Each storage slot holds a small linked list of every item that landed there — so a collision just adds another link in that slot's chain
- **Open Addressing:** When a slot is already taken, the system searches for the next available slot using a predictable pattern

---

## When to Use Each Data Structure

| Structure | Best for |
|---|---|
| **Lists** | Ordered, indexed access when you don't know the size upfront |
| **Stacks** | LIFO needs — undo functionality, expression evaluation, backtracking |
| **Queues** | FIFO needs — task scheduling, breadth-first search |
| **Linked Lists** | Frequent insert/delete at the beginning, unknown size, no need for random access |
| **Hash Maps** | Fast key-value lookups, counting occurrences, caching |
| **Sets** | Uniqueness checks, mathematical set operations, removing duplicates |

---

## Solid Foundation!

You now understand not just *how* to use these structures, but *why* you'd reach for one over another — which is exactly the kind of thinking that separates "I can write code" from "I can write efficient code." Big O especially will keep paying off the deeper you go into more advanced algorithms and technical interviews.

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
