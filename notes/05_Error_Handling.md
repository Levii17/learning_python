# Error Handling — The Beginner-Friendly Guide

> How to read Python's error messages, hunt down bugs, and build code that fails gracefully instead of crashing.

---

## Table of Contents

1. [Common Errors in Python](#-common-errors-in-python)
2. [Good Debugging Techniques](#-good-debugging-techniques)
3. [Exception Handling: try / except / else / finally](#-exception-handling-try--except--else--finally)
4. [The Exception Object](#-the-exception-object)
5. [The raise Statement](#-the-raise-statement)
6. [Custom Exceptions](#-custom-exceptions)
7. [Chaining Exceptions with raise ... from](#-chaining-exceptions-with-raise--from)
8. [assert Statements](#-assert-statements)

---

## Common Errors in Python

**Simple definition:** An error message is Python's way of telling you — often quite precisely — exactly what went wrong and where.

**Analogy:** Think of an error message like a "check engine" light with a specific diagnostic code, rather than just a vague red light. If you learn to read the codes, you can usually pinpoint the problem in seconds instead of guessing.

| Error | When it happens | Example |
|---|---|---|
| **SyntaxError** | Your code breaks Python's grammar rules | Missing a closing parenthesis |
| **NameError** | You use a variable/function that was never defined | Typo'd variable name, or used before assignment |
| **TypeError** | You mix incompatible data types in an operation | Adding a string and a number |
| **IndexError** | You reference a position that doesn't exist in a sequence | Accessing index `5` in a 3-item list |
| **AttributeError** | You call a method that doesn't exist for that data type | Calling `.append()` on a string |

```python
# SyntaxError — missing closing parenthesis
print("Hello, world!")
# SyntaxError: unexpected EOF while parsing
```

```python
# NameError — variable was never defined
print(name)
# NameError: name 'name' is not defined
```

```python
# TypeError — can't add a string and an integer directly
5 + "5"
# TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

```python
# IndexError — list only has indices 0, 1, 2
my_list = [1, 2, 3]
print(my_list[5])
# IndexError: list index out of range
```

```python
# AttributeError — integers don't have an .append() method
num = 42
num.append(5)
# AttributeError: 'int' object has no attribute 'append'
```

> **Golden rule of debugging:** Read the full error message before guessing. Python almost always tells you the error *type*, the *file and line number*, and often the *exact reason* — that's your map straight to the bug.

---

## Good Debugging Techniques

**Simple definition:** Debugging is the process of tracking down why your code isn't doing what you expect, and fixing it.

**Analogy:** Debugging is like being a detective investigating a scene — `print()` statements are like quick notes jotted at each checkpoint, `pdb` is like pausing the scene entirely to interview each witness (variable) in real time, and an IDE debugger is like having security camera footage you can rewind, pause, and zoom into.

### 1. print() Statements — the quick-and-easy option
```python
def add(a, b):
    result = a + b
    print(f'Adding {a} and {b} gives {result}')  # peek at values as they happen
    return result
```
Great for a fast sanity check on variable values and code flow.

### 2. Python's Built-in Debugger — pdb
**Simple definition:** `pdb` lets you pause your program mid-execution and poke around — checking variable values, types, and stepping line by line — all from the terminal.

```python
import pdb

def divide(a, b):
    pdb.set_trace()  # execution pauses here
    return a / b

print(divide(10, 2))
```

When it hits `set_trace()`, you'll drop into an interactive prompt:
```
> /Users/fcc/Desktop/debugging.py(5)divide()
-> return a / b
(Pdb)
```

Handy commands once you're in the prompt:
- `whatis a` → shows the type of variable `a`
- `continue` (or `c`) → resumes running the code
- `help` → lists every available command

```
(Pdb) whatis a
<class 'int'>
(Pdb) continue
5.0
```

### 3. IDE Debugging Tools (e.g., VS Code)
**Analogy:** This is the "security footage" option — a visual way to pause execution and watch every variable update in real time.

Quick walkthrough in VS Code:
1. Click in the gutter (left margin) next to a line to set a **breakpoint** (a red dot appears)
2. Press **F5** to start debugging
3. Execution pauses at your breakpoint — hover over variables to see their current values
4. Use the debug toolbar:
   - **Continue (F5)** — resume until the next breakpoint
   - **Step Over (F10)** — run the current line, move to the next
   - **Step Into (F11)** — dive into a function call
   - **Step Out (Shift+F11)** — exit the current function

> **Which one should I use?** `print()` for a fast check, `pdb` for interactive terminal-based exploration, and IDE tools when you want a full visual picture — all three are worth knowing.

---

## Exception Handling: try / except / else / finally

**Simple definition:** Exception handling lets you anticipate that something *might* go wrong, and decide exactly how your program should respond instead of crashing.

**Analogy:** It's like a safety net under a tightrope walker — you're not preventing every possible slip, but you're making sure a slip doesn't end the show. `try` is the tightrope walk, `except` is the net catching a specific kind of fall, `else` is the applause when nothing goes wrong, and `finally` is the crew that packs up the equipment no matter how the act ended.

```python
try:
    print(22 / 0)
except ZeroDivisionError:
    print("You can't divide by zero!")
    # You can't divide by zero!
```

### Handling Multiple Error Types
```python
try:
    number = int(input('Enter a number: '))
    print(22 / number)
except ZeroDivisionError:
    print('You cannot divide by zero!')     # runs if you enter 0
except ValueError:
    print('Please enter a valid number!')   # runs if you enter a non-number, like "abc"
```

You can also catch several exception types with a single `except` by grouping them in a tuple:
```python
try:
    number = int(input('Enter a number: '))
    result = 10 / number
except (ValueError, ZeroDivisionError) as e:
    print(f'Error occurred: {e}')
```

### else and finally
```python
try:
    result = 100 / 4
except ZeroDivisionError:
    print('You cannot divide by zero!')  # skipped — no error occurred
else:
    print(f'Result is {result}')          # Result is 25.0 → runs only if NO exception happened
finally:
    print('Execution complete!')          # ALWAYS runs, error or not
```

> **When to use `finally`:** Perfect for cleanup work — closing files, releasing network connections, etc. — things that must happen no matter what.

---

## The Exception Object

**Simple definition:** Using `as` lets you capture the actual exception object, so you can inspect or print its specific error message.

**Analogy:** Instead of just being told "something broke," this is like getting the actual incident report with full details of exactly what happened.

```python
try:
    value = int('This will raise an error')
except ValueError as e:
    print(f'Caught an error: {e}')
    # Caught an error: invalid literal for int() with base 10: 'This will raise an error'
```

---

## The raise Statement

**Simple definition:** `raise` lets you manually trigger an exception yourself — useful for enforcing rules or flagging invalid input before it causes bigger problems.

**Analogy:** `raise` is like a lifeguard blowing a whistle the moment someone breaks a pool rule — you're not waiting for a real accident to happen; you're stopping things proactively the instant a condition is violated.

```python
def check_age(age):
    if age < 0:
        raise ValueError('Age cannot be negative')
    return age

try:
    check_age(-5)
except ValueError as e:
    print(f'Error: {e}')  # Error: Age cannot be negative
```

### Re-raising an Exception
Calling `raise` with no arguments inside an `except` block re-throws the *same* exception — handy when you want to log something but still let the error propagate upward.

```python
def process_data(data):
    try:
        result = int(data)
        return result * 2
    except ValueError:
        print('Logging: Invalid data received')
        raise  # re-raises the SAME ValueError

try:
    process_data('abc')
except ValueError:
    print('Handled at higher level')
```

---

## Custom Exceptions

**Simple definition:** You can design your own exception types by creating a class that inherits from `Exception` — useful when the built-in error types don't describe your specific problem clearly enough.

**Analogy:** Built-in exceptions are like generic warning labels ("Caution: Hot"). A custom exception is like a label written specifically for your product ("Caution: Battery Overheating Risk") — more specific, more useful to whoever reads it.

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f'Insufficient funds: ${balance} available, ${amount} requested')

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    new_balance = withdraw(100, 150)
except InsufficientFundsError as e:
    print(f'Transaction failed: {e}')
    # Transaction failed: Insufficient funds: $100 available, $150 requested
```

Another example — a login system with a custom credentials error:
```python
class InvalidCredentialsError(Exception):
    def __init__(self, message="Invalid username or password"):
        self.message = message
        super().__init__(self.message)

def login(username, password):
    stored_username = "admin"
    stored_password = "password123"

    if username != stored_username or password != stored_password:
        raise InvalidCredentialsError()

    return f"Welcome, {username}!"

try:
    message = login("user", "wrongpassword")
except InvalidCredentialsError as e:
    print(f"Login failed: {e}")
else:
    print(message)  # only runs if login succeeded
```

> Don't worry if `class` and `__init__` look unfamiliar — you'll cover classes and inheritance in more depth soon. For now, just know this is how custom exceptions get built.

---

## Chaining Exceptions with raise ... from

**Simple definition:** `raise ... from` lets you connect a new exception to the original one that caused it — either hiding the original (`from None`) or preserving the full trail (`from e`).

**Analogy:** `from e` is like keeping a paper trail showing "this problem happened *because of* that earlier problem" — useful for tracing root causes. `from None` is like saying "trust me, just look at this new explanation and ignore the earlier mess."

```python
def parse_config(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            return int(data)
    except FileNotFoundError:
        raise ValueError('Configuration file is missing') from None
    except ValueError as e:
        raise ValueError('Invalid configuration format') from e

config = parse_config('config.txt')
```

- `raise ... from None` → suppresses the original traceback, showing only your new, cleaner message
- `raise ... from e` → keeps both tracebacks, showing "the above exception was the direct cause of the following exception"

---

## assert Statements

**Simple definition:** `assert` is a shorthand way to raise an `AssertionError` if a condition turns out to be `False` — a quick sanity check embedded directly in your code.

**Analogy:** An `assert` is like a pre-flight checklist step — "assert the fuel tank isn't empty" — if the condition fails, everything stops immediately rather than continuing into a bigger disaster.

```python
def calculate_square_root(number):
    assert number >= 0, 'Cannot calculate square root of negative number'
    return number ** 0.5

try:
    result = calculate_square_root(-4)
except AssertionError as e:
    print(f'Assertion failed: {e}')
    # Assertion failed: Cannot calculate square root of negative number
```

> `assert` is best for catching programming mistakes and invariants during development — not for validating user input in production code (asserts can be stripped out under certain optimization settings).

---

## Nicely Done!

You now know how to read Python's error messages instead of fearing them, debug methodically instead of guessing, and build programs that handle failure gracefully with `try`/`except`/`else`/`finally`, custom exceptions, and `raise`. This is one of the biggest signals of a maturing developer — bugs stop being scary and start being solvable.

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
