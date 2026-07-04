# Object-Oriented Programming — The Beginner-Friendly Guide

> The four pillars of OOP — encapsulation, inheritance, polymorphism, and abstraction — explained without the jargon overload.

---

## Table of Contents

1. [What is Object-Oriented Programming?](#-what-is-object-oriented-programming)
2. [Encapsulation](#-encapsulation)
3. [Getters, Setters & Properties](#-getters-setters--properties)
4. [Inheritance](#-inheritance)
5. [Polymorphism](#-polymorphism)
6. [Name Mangling](#-name-mangling)
7. [Abstraction](#-abstraction)

---

## What is Object-Oriented Programming?

**Simple definition:** OOP is a style of programming where you model your code around real-world "objects" — things with data (attributes) and behavior (methods) — rather than just a long list of instructions.

**Analogy:** Instead of writing one giant recipe for an entire restaurant, OOP is like designing individual staff roles — a chef object, a waiter object, a cashier object — each with their own responsibilities and information, all working together.

The four pillars of OOP:
- **Encapsulation** — bundling and protecting data
- **Inheritance** — reusing code across related classes
- **Polymorphism** — same method name, different behavior per class
- **Abstraction** — hiding complexity, showing only what's needed

---

## Encapsulation

**Simple definition:** Encapsulation means bundling data and the methods that operate on it together, while hiding the internal details from outside interference.

**Analogy:** Think of encapsulation like a bank's ATM. You can deposit and withdraw money through a simple, controlled interface (the screen and buttons), but you can't reach in and directly rearrange the cash inside the vault. The "doors" (public methods) control access; what's "behind the doors" (private data) stays protected.

```python
class Wallet:
    def __init__(self, balance):
        self.__balance = balance  # double underscore = private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount  # controlled, safe change

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount  # controlled, safe change

account = Wallet(500)
print(account.__balance)
# AttributeError: 'Wallet' object has no attribute '__balance'
```

> Even though it's "private," the balance can still be changed safely — just only through the `deposit()` and `withdraw()` doors, which enforce sensible rules (like never allowing a negative balance).

### Single Underscore vs Double Underscore

| Prefix | Meaning | Enforced? |
|---|---|---|
| `_attribute` | "Internal use, please don't touch" | Just a convention — nothing stops you |
| `__attribute` | Actively hidden from outside access | Python blocks direct outside access |

---

## Getters, Setters & Properties

**Simple definition:** Getters retrieve a value, setters assign one — and **properties** let you do both while still using simple dot notation (no parentheses), plus run extra validation behind the scenes.

**Analogy:** A property is like a thermostat display — you just read the number or turn the dial, but internally, the thermostat is running checks (is this temperature safe? within range?) that you never see.

### Creating a Getter
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):  # getter — runs when you READ my_circle.radius
        return self._radius

    @property
    def area(self):  # getter can also compute something on the fly
        return 3.14 * (self._radius ** 2)

my_circle = Circle(3)

print(my_circle.radius)  # 3      → no parentheses needed!
print(my_circle.area)    # 28.26
```

### Creating a Setter
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):  # setter — runs when you ASSIGN my_circle.radius = ...
        if value <= 0:
            raise ValueError('Radius must be positive')
        self._radius = value

my_circle = Circle(3)
print('Initial radius:', my_circle.radius)  # Initial radius: 3

my_circle.radius = 8  # this LOOKS like a plain assignment, but the setter runs behind it
print('After modifying the radius:', my_circle.radius)  # After modifying the radius: 8
```

> **Common trap:** Inside the setter, never write `self.radius = value` — that would call the setter *again*, forever, causing a `RecursionError`. Always store the real value under a different name (like `self._radius`).

### Deleters
```python
class Circle:
    # ... getter and setter above ...

    @radius.deleter
    def radius(self):
        print("Deleting radius...")
        del self._radius
```

**Why bother with properties instead of plain methods?** Because `my_circle.radius` reads far more naturally than `my_circle.get_radius()` — it looks like a simple attribute, while still giving you full control (validation, computed values, cleanup logic) under the hood.

---

## Inheritance

**Simple definition:** Inheritance lets a "child" class automatically pick up the attributes and methods of a "parent" class — so you don't have to rewrite shared logic from scratch.

**Analogy:** Inheritance is like inheriting traits from a parent — you're born with certain baseline features (eye color, height range), but you can still develop your own unique personality on top of that foundation.

```python
class Parent:
    pass  # attributes and methods for Parent

class Child(Parent):
    pass  # Child automatically inherits everything from Parent
    # ...and can add or override its own behavior too
```

### Single vs Multiple Inheritance
```python
# Single inheritance — one parent
class Child(Parent):
    pass

# Multiple inheritance — more than one parent
class Parent:
    pass

class OtherParent:
    pass

class GrandChild(Parent, OtherParent):
    pass  # inherits from BOTH — can combine or override behavior from each
```

### The super() Function
**Simple definition:** `super()` lets a child class call a method from its parent — useful when you want to *extend* the parent's behavior rather than fully replace it.

**Analogy:** `super()` is like building on your parent's family recipe instead of starting from scratch — you keep their base steps, then add your own twist on top.

---

## Polymorphism

**Simple definition:** Polymorphism means different classes can share the same method name, but each class implements that method in its own way.

**Analogy:** Think of the word "start" — you "start" a car by turning a key, "start" a computer by pressing a power button, and "start" a conversation by saying hello. Same word, completely different actions depending on the "class" of thing you're starting.

```python
class A:
    def action(self):
        print('A is acting')

class B:
    def action(self):
        print('B is acting differently')

class C:
    def action(self):
        print('C does its own thing')

# Same method name, different behavior — regardless of which object calls it
for obj in [A(), B(), C()]:
    obj.action()
```

**Inheritance-based polymorphism:** A parent class sets up a method, and each child class "twists" it to fit its own needs — this is one of the most common ways polymorphism shows up in real code.

---

## Name Mangling

**Simple definition:** When you prefix an attribute with a double underscore, Python secretly renames it behind the scenes — turning `__data` into `_ClassName__data` — to avoid accidental clashes between parent and child classes.

**Analogy:** Imagine two family members both nicknamed "Junior." Name mangling is like automatically tagging each one with their family surname behind the scenes ("Smith Junior," "Jones Junior") so nobody accidentally overwrites the other's stuff, even though they're both just called "Junior" out loud.

```python
class Parent:
    def __init__(self):
        self.__data = 'Parent data'

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__data = 'Child data'

c = Child()
print(c.__dict__)
# {'_Parent__data': 'Parent data', '_Child__data': 'Child data'}
```

Notice both `__data` attributes survive separately — name mangling silently prevented the child's version from wiping out the parent's.

---

## Abstraction

**Simple definition:** Abstraction means hiding complex implementation details and exposing only the essential parts someone actually needs to interact with.

**Analogy:** Driving a car is the classic example — you interact with the wheel, pedals, and gear shifter, without ever needing to understand engine combustion or brake hydraulics. The complexity is there, just hidden behind a simple interface.

### How Python Implements It: the abc Module
**Simple definition:** An **abstract base class (ABC)** defines methods that every subclass *must* implement — but the abstract class itself can never be directly instantiated.

```python
from abc import ABC, abstractmethod

# Define an abstract base class — this is a "template contract"
class AbstractClass(ABC):
    @abstractmethod
    def abstract_method(self):
        pass  # no implementation here — subclasses MUST provide their own

# Concrete subclass #1 — fulfills the contract
class ConcreteClassOne(AbstractClass):
    def abstract_method(self):
        print('Implementation in ConcreteClassOne')

# Concrete subclass #2 — fulfills the contract differently
class ConcreteClassTwo(AbstractClass):
    def abstract_method(self):
        print('Implementation in ConcreteClassTwo')
```

> Trying to create `AbstractClass()` directly would raise a `TypeError` — it exists purely to enforce that any subclass built from it *must* implement `abstract_method()`, guaranteeing a consistent interface across all subclasses.

---

## You've Got the Full Picture!

You've now covered all four pillars of Object-Oriented Programming — encapsulation to protect data, inheritance to reuse code, polymorphism to share method names flexibly, and abstraction to hide complexity behind clean interfaces. Together, these concepts are what let large, real-world codebases stay organized and maintainable instead of collapsing into spaghetti code. This is genuinely advanced-beginner territory — nice work getting here! 

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
