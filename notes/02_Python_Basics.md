# Python Basics , The Beginner-Friendly Guide

> A scannable, analogy-packed reference for anyone learning Python from scratch. Skim it, bookmark it, come back to it.

---

## Table of Contents

1. [What is Python?](#-what-is-python)
2. [Variables](#-variables)
3. [Comments](#-comments)
4. [Common Data Types](#-common-data-types)
5. [Mutable vs Immutable](#-mutable-vs-immutable)
6. [Working with Strings](#-working-with-strings)
7. [Common String Methods](#-common-string-methods)
8. [Numbers: Ints & Floats](#-numbers-ints--floats)
9. [Augmented Assignment](#-augmented-assignment)
10. [Functions](#-functions)
11. [Common Built-in Functions](#-common-built-in-functions)
12. [Scope](#-scope)
13. [Comparison Operators](#-comparison-operators)
14. [if / elif / else](#-if--elif--else)
15. [Truthy & Falsy Values](#-truthy--falsy-values)
16. [Boolean Operators & Short-Circuiting](#-boolean-operators--short-circuiting)

---

## What is Python?

**Simple definition:** Python is a programming language built to be readable and easy to write , it reads almost like plain English.

**Analogy:** If programming languages were vehicles, Python is the reliable, easy-to-drive automatic car , you don't need to know how the engine works to get where you're going. (C is the manual transmission sports car , faster in the right hands, but a lot more to manage.)

**Where it's used:**
- Data science & machine learning
- Web development
- Cybersecurity
- Automation & scripting
- Microcomputers (Raspberry Pi, MicroPython boards)

---

## Variables

**Simple definition:** A variable is a labeled container that holds a value so you can use it later.

**Analogy:** Think of a variable like a labeled storage box. You write a name on the box (`age`), put something inside it (`25`), and now you can grab that box any time just by calling its name.

```python
# Creating variables: name = value
name = 'John Doe'   # box labeled "name" holds a string
age = 25             # box labeled "age" holds a number
```

### Naming Rules Cheat Sheet
- Must start with a letter or underscore , never a number
- Can only contain letters, numbers, and underscores
- Case-sensitive → `age`, `Age`, and `AGE` are three *different* boxes
- Can't use reserved keywords (`if`, `class`, `def`, etc.)
- Multi-word names use `snake_case` → `first_name`

---

## Comments

**Simple definition:** Comments are notes in your code that Python ignores when running , they're for humans, not the computer.

**Analogy:** Comments are like sticky notes on a recipe card , they don't change the dish, but they remind you (or a teammate) why you did something a certain way.

```python
# This is a single-line comment , great for quick notes

"""
This is a multi-line string.
Handy for longer notes, or for temporarily
"commenting out" a whole block of code:

name = 'John Doe'
age = 25
"""

print('Hello world!')  # Hello world!
```

---

## Common Data Types

**Simple definition:** A data type tells Python *what kind* of value you're working with (a number, text, true/false, etc.), which determines what you can do with it.

**Analogy:** Data types are like different kinds of containers in a kitchen , you wouldn't pour soup into a colander or store ice cream in an open bowl. Each container (type) is suited to a specific job.

> Python is **dynamically-typed** , like JavaScript, you never have to declare a type up front. Python figures it out from the value you assign.

| Type | What it is | Example |
|---|---|---|
| **Integer** | Whole number, no decimals | `my_int = 10` |
| **Float** | Number with decimals | `my_float = 4.50` |
| **String** | Text, wrapped in quotes | `my_str = 'hello'` |
| **Boolean** | True or False | `is_valid = True` |
| **Set** | Unordered, *unique* items only | `{7, 5, 8}` |
| **Dictionary** | Key-value pairs | `{"name": "Alice", "age": 25}` |
| **Tuple** | Ordered, cannot be changed | `(7, 5, 8)` |
| **Range** | Sequence of numbers, used in loops | `range(5)` |
| **List** | Ordered collection, mixed types OK | `[22, 'Hi', 3.14, True]` |
| **None** | Represents "nothing here" | `my_none = None` |

```python
my_dictionary_var = {"name": "Alice", "age": 25}
print('Dictionary:', my_dictionary_var)
# Dictionary: {'name': 'Alice', 'age': 25}
```

---

## Mutable vs Immutable

**Simple definition:** *Immutable* means "can't be changed once created." *Mutable* means "can be changed after creation."

**Analogy:** An immutable type is like a can of soda , once it's sealed, you can't edit what's inside; you can only replace it with a whole new can. A mutable type is like a whiteboard , you can erase and rewrite parts of it anytime without replacing the whole board.

- **Immutable:** `int`, `float`, `complex`, `bool`, `string`, `tuple`, `range`, `None`
- **Mutable:** `list`, `set`, `dictionary`

```python
greeting = 'Hello there!'
age = 21

print(type(greeting))  # <class 'str'>
print(type(age))       # <class 'int'>

# isinstance() checks if a value matches a type
print(isinstance(greeting, str))  # True
print(isinstance(age, str))       # False
```

---

## Working with Strings

**Simple definition:** A string is a sequence of characters , basically, text.

**Analogy:** A string is like a row of labeled mailboxes on a street , each character has its own numbered "address" (index), so you can walk right up to any specific letter.

```python
my_str = 'Hello world'

print(my_str[0])   # H   → first character
print(my_str[6])   # w   → 7th character (indexing starts at 0!)
print(my_str[-1])  # d   → last character (negative counts from the end)
```

### Escaping Quotes
```python
msg = 'It\'s a sunny day'          # backslash "escapes" the quote
quote = "She said, \"Hello!\""
```

### Concatenation (joining strings)
```python
developer = 'Jessica'
print('My name is ' + developer + '.')  # My name is Jessica.

# += glues and re-assigns in one step
greeting = 'My name is '
greeting += 'Jessica.'
print(greeting)  # My name is Jessica.
```

### f-strings (the modern, clean way)
**Analogy:** f-strings are like mail-merge templates , you write the sentence once with blanks, and Python fills in the blanks for you.

```python
developer = 'Jessica'
greeting = f'My name is {developer}.'
print(greeting)  # My name is Jessica.
```

### Slicing: `str[start:stop:step]`
**Analogy:** Slicing a string is like cutting a specific-length ribbon from a spool , you say where to start cutting, where to stop, and whether to skip every-other-inch.

```python
message = 'Python is fun!'

print(message[0:6])   # Python   → from index 0 up to (not including) 6
print(message[7:])    # is fun!  → from index 7 to the end
print(message[::2])   # Pto sfn  → every 2nd character
```

### Length & Membership
```python
developer = 'Jessica'
print(len(developer))          # 7

my_str = 'Hello world'
print('Hello' in my_str)       # True  → is 'Hello' inside the string?
print('hey' in my_str)         # False
```

---

## Common String Methods

Think of these as pre-built "tools" that come attached to every string.

| Method | What it does | Example |
|---|---|---|
| `.upper()` | ALL CAPS | `'hi'.upper()` → `'HI'` |
| `.lower()` | all lowercase | `'HI'.lower()` → `'hi'` |
| `.strip()` | Removes leading/trailing whitespace | `'  hi  '.strip()` → `'hi'` |
| `.replace(old, new)` | Swaps text | `'hi'.replace('h','p')` → `'pi'` |
| `.split(sep)` | Breaks a string into a list | `'a-b'.split('-')` → `['a','b']` |
| `.join(list)` | Glues a list into one string | `' '.join(['a','b'])` → `'a b'` |
| `.startswith(x)` | Checks the beginning | `'Naomi'.startswith('N')` → `True` |
| `.endswith(x)` | Checks the ending | `'Naomi'.endswith('N')` → `False` |
| `.find(x)` | Index of first match (or `-1`) | `'Naomi'.find('N')` → `0` |
| `.count(x)` | Counts occurrences | `'Los Angeles'.count('e')` → `2` |
| `.capitalize()` | Capitalizes first letter only | `'cake'.capitalize()` → `'Cake'` |
| `.title()` | Capitalizes every word | `'los angeles'.title()` → `'Los Angeles'` |
| `.isupper()` / `.islower()` | Checks casing | `'HI'.isupper()` → `True` |

```python
dashed_name = 'example-dashed-name'
split_words = dashed_name.split('-')
print(split_words)  # ['example', 'dashed', 'name']

joined_str = ' '.join(split_words)
print(joined_str)   # example dashed name
```

---

## Numbers: Ints & Floats

**Simple definition:** Basic math in Python works the way you'd expect from a calculator , plus a few extra handy operators.

**Analogy:** Think of `//` (floor division) as splitting a pizza into whole slices only , no fractional slice, and `%` (modulo) as the crumbs left over once you've cut as many whole slices as you can.

```python
int_1 = 56
int_2 = 12

print(int_1 + int_2)   # 68   → addition
print(int_1 - int_2)   # 44   → subtraction
print(int_1 * int_2)   # 672  → multiplication
print(int_1 / int_2)   # 4.666666666666667  → division (always returns a float)
print(int_1 % int_2)   # 8    → modulo: the remainder
print(int_1 // int_2)  # 4    → floor division: rounds down to whole number
print(int_1 ** 2)      # 3136 → exponent: raise to the power of
```

> Mixing an `int` and a `float` in an operation always upgrades the result to a `float`:
> `56 + 5.4` → `61.4`

### Handy Number Functions
```python
print(float(4))       # 4.0   → int to float
print(int(4.0))       # 4     → float to int
print(round(3.4))     # 3     → nearest whole number
print(round(7.7))     # 8
print(abs(-13))       # 13    → absolute (always positive) value
print(pow(2, 3))      # 8     → same as 2 ** 3
```

---

## ⚡ Augmented Assignment

**Simple definition:** A shorthand that combines "do the math" and "save the result" into one line.

**Analogy:** Instead of writing "take the amount in my wallet, add $5, then put that new total back in my wallet" , you just say "add $5 to my wallet." Same result, less typing.

```python
my_var = 10
my_var += 5     # same as: my_var = my_var + 5
print(my_var)   # 15

price = 100
price /= 4      # same as: price = price / 4
print(price)    # 25.0
```

Other augmented operators: `-=`, `*=`, `//=`, `%=`, `**=` (and bitwise ones: `&=`, `^=`, `>>=`, `<<=`)

---

## Functions

**Simple definition:** A function is a reusable block of code that takes some input, does something with it, and (optionally) hands back a result.

**Analogy:** A function is like a vending machine , you put something in (money/arguments), it does its internal work, and something comes out (a snack/return value). You don't need to know the machine's insides to use it.

```python
# Defining a function
def get_sum(num_1, num_2):
    return num_1 + num_2

result = get_sum(3, 4)  # calling the function
print(result)           # 7
```

**Good to know:**
- If a function has no `return`, it hands back `None` by default.
- You can set **default values** for parameters:

```python
def get_sum(num_1, num_2=2):  # num_2 defaults to 2 if not given
    return num_1 + num_2

print(get_sum(3))  # 5
```

- Calling a function with the wrong number of arguments raises a `TypeError`:

```python
def calculate_sum(a, b):
    print(a + b)

calculate_sum()
# TypeError: calculate_sum() missing 2 required positional arguments: 'a' and 'b'
```

---

## Common Built-in Functions

**Simple definition:** Ready-made functions Python gives you for free , no need to build them yourself.

```python
name = input('What is your name? ')  # pauses and waits for user input
print('Hello', name)

print(int(3.14))    # 3     → converts to integer
print(int('42'))    # 42    → converts numeric string to integer
print(int(True))    # 1     → True becomes 1
print(int(False))   # 0     → False becomes 0
```

---

## Scope

**Simple definition:** Scope determines *where* in your code a variable can be seen and used.

**Analogy:** Scope is like rooms in a house. A **local** variable only exists in the room (function) it was created in. A **global** variable is like something posted on the front door , visible from anywhere in the house. An **enclosing** scope is like a smaller room nested inside a bigger one , the inner room can see what's on the bigger room's shelf, but not vice versa.

```python
# Local scope , only visible inside my_func
def my_func():
    num = 10
    print(num)

# Enclosing scope , inner_func can "see" msg from outer_func
def outer_func():
    msg = 'Hello there!'
    def inner_func():
        print(msg)
    inner_func()

outer_func()  # Hello there!

# Global scope , visible everywhere
tax = 0.70
def get_total(subtotal):
    return subtotal + (subtotal * tax)

print(get_total(100))  # 170.0

# Built-in scope , Python's own reserved names
print(str(45))            # '45'
print(type(3.14))         # <class 'float'>
```

---

## Comparison Operators

**Simple definition:** These operators compare two values and give back `True` or `False`.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | Equal to | `3 == 4` | `False` |
| `!=` | Not equal to | `3 != 4` | `True` |
| `>` | Greater than | `3 > 4` | `False` |
| `<` | Less than | `3 < 4` | `True` |
| `>=` | Greater than or equal to | `3 >= 4` | `False` |
| `<=` | Less than or equal to | `3 <= 4` | `True` |

---

## if / elif / else

**Simple definition:** These let your program make decisions , "if this is true, do that; otherwise, try something else."

**Analogy:** It's a traffic light for your code's logic: green (`if`) means go this way, yellow (`elif`) is your backup route, red (`else`) is the fallback if nothing else applied.

```python
age = 16

if age >= 18:
    print('You are an adult')
elif age >= 13:                  # only checked if the first was False
    print('You are a teenager')  # this runs
else:
    print('You are a child')
```

**Nested conditionals** (an `if` inside another `if`):
```python
is_citizen = True
age = 25

if is_citizen:
    if age >= 18:
        print('You are eligible to vote')  #  this runs
else:
    print('You are not eligible to vote')
```

---

## Truthy & Falsy Values

**Simple definition:** Every value in Python has a built-in "truthiness" , even if it's not an actual boolean, Python can treat it as `True` or `False` in a logical context.

**Analogy:** Think of it like an "is there anything here?" check. An empty box, a zero balance, or silence all read as "no" (falsy) , anything with actual content reads as "yes" (truthy).

**Falsy values:** `None`, `False`, `0`, `0.0`, `''` (empty string)

**Everything else is truthy** , non-zero numbers, non-empty strings, etc.

```python
print(bool(False))  # False
print(bool(0))       # False
print(bool(''))      # False

print(bool(True))    # True
print(bool(1))       # True
print(bool('Hello')) # True
```

---

## Boolean Operators & Short-Circuiting

**Simple definition:** `and`, `or`, and `not` let you combine or flip logical conditions.

**Analogy:**
- `and` is like a two-key safe , both keys must turn for it to open.
- `or` is like a door with two doorbells , ring either one and someone answers.
- `not` is a light switch , it flips whatever state you're in.

```python
# and → both must be truthy
is_citizen = True
age = 25
if is_citizen and age >= 18:
    print('You are eligible to vote')  # runs , both are truthy

# or → at least one must be truthy
age = 19
is_student = True
if age < 18 or is_student:
    print('You are eligible for a student discount')  # runs

# not → flips True to False and vice versa
is_admin = False
if not is_admin:
    print('Access denied for non-administrators.')  # runs
```

**Short-circuiting:** Python reads `and`/`or` left to right and stops the moment it knows the answer , just like you'd stop reading a sentence once you already know how it ends.

---

## You Made It!

You've now covered the real building blocks of Python , variables, data types, strings, numbers, functions, scope, and logic. Every advanced concept you'll learn next (loops, classes, error handling) is built on top of exactly this foundation. Keep going!

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
