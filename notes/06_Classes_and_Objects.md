# Classes & Objects

> The building blocks of Object-Oriented Programming , blueprints, instances, and the "magic" methods that power Python's built-in behaviors.

---

## Table of Contents

1. [Class Definitions](#-class-definitions)
2. [Creating Objects](#-creating-objects)
3. [Class vs Object](#-class-vs-object)
4. [Attributes: Instance vs Class](#-attributes-instance-vs-class)
5. [Methods](#-methods)
6. [Dunder (Magic) Methods](#-dunder-magic-methods)
7. [Real-World Example: Shopping Cart](#-real-world-example-shopping-cart)

---

## Class Definitions

**Simple definition:** A class is a blueprint that describes what an object should look like and what it can do , its data (attributes) and its behavior (methods).

**Analogy:** A class is like a cookie cutter , it's not a cookie itself, it's the *shape* that gets used to stamp out actual cookies (objects). Every cookie made from the same cutter shares the same shape, but each one is still its own individual cookie.

```python
class Dog:
    def __init__(self, name, age):  # runs automatically when a new Dog is created
        self.name = name             # store the given name on this specific dog
        self.age = age                # store the given age on this specific dog

    def bark(self):
        print(f'{self.name.upper()} says woof woof!')
```

> `__init__` is the **constructor** , think of it as the setup instructions that run the moment a new object is stamped out from the blueprint. `self` refers to "this specific object," so every dog keeps its own name and age separate from every other dog.

---

## Creating Objects

**Simple definition:** An object is a real, individual instance created from a class , with its own actual data.

**Analogy:** If the `Dog` class is the cookie cutter, then `dog1` and `dog2` are two actual cookies made from it , same shape, but each is a separate cookie you could eat (or, in this case, pet) independently.

```python
dog1 = Dog('Jack', 3)
dog2 = Dog('Thatcher', 5)

dog1.bark()  # JACK says woof woof!
dog2.bark()  # THATCHER says woof woof!
```

**Calling methods** on an object uses dot notation:
```python
object_name1.method_name()
object_name2.method_name()
```

---

## Class vs Object

**Simple definition:**
- **Class** = the reusable template/design
- **Object** = one specific thing built from that template, holding real data

| | Class | Object |
|---|---|---|
| What it is | The blueprint | An actual instance |
| Example | `Dog` | `dog1 = Dog('Jack', 3)` |
| Analogy | The cookie cutter | An actual cookie |

---

## Attributes: Instance vs Class

**Simple definition:**
- **Instance attributes** , unique data belonging to *one specific* object, set up in `__init__` using `self`
- **Class attributes** , shared data that's the *same for every object* made from that class

**Analogy:** Think of a litter of French Bulldog puppies. Their **breed** ("French Bulldog") is identical for every single one , that's a class attribute, defined once and shared. But each puppy's **name** is unique to that individual puppy , that's an instance attribute.

```python
class Dog:
    species = 'French Bulldog'  # Class attribute , shared by ALL dogs

    def __init__(self, name):
        self.name = name  # Instance attribute , unique to THIS dog

print(Dog.species)  # French Bulldog → accessible directly from the class

jack = Dog('Jack')
print(jack.name)     # Jack
print(jack.species)  # French Bulldog → inherited from the class
```

---

## Methods

**Simple definition:** A method is just a function that lives inside a class and operates on that object's own data.

**Analogy:** If an object is a car, its methods are the actions the car can perform using its own current state , honking, describing its own color and model, etc. The action always references *this specific car's* details, not some generic car.

```python
class Car:
    def __init__(self, color, model):
        self.color = color
        self.model = model

    def describe(self):
        return f'This car is a {self.color} {self.model}'

my_car_1 = Car('red', 'Tesla Model S')
print(my_car_1.describe())  # This car is a red Tesla Model S
```

### Calling Methods on Multiple Objects
Each object keeps its own data, so the same method call produces different results depending on *which* object called it:

```python
my_car_1 = Car('red', 'Tesla Model S')
my_car_2 = Car('green', 'Lamborghini Revuelto')

print(my_car_1.describe())  # This car is a red Tesla Model S
print(my_car_2.describe())  # This car is a green Lamborghini Revuelto
```

---

## Dunder (Magic) Methods

**Simple definition:** Special methods surrounded by double underscores (like `__init__`, `__len__`, `__str__`) that Python calls automatically behind the scenes for built-in operations , you rarely call them directly yourself.

**Analogy:** Dunder methods are like universal remote-control buttons. You never open up the TV and manually flip a switch inside , you just press "power" or "volume up," and the TV knows exactly what internal action that corresponds to. Similarly, you just write `len(book1)` and Python automatically knows to run that object's `__len__` behavior behind the scenes.

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __len__(self):
        return self.pages

    def __str__(self):
        return f"'{self.title}' has {self.pages} pages"

    def __eq__(self, other):
        return self.pages == other.pages

book1 = Book('Built Wealth Like a Boss', 420)

print(len(book1))  # 420   → Python calls __len__ behind the scenes
print(str(book1))  # 'Built Wealth Like a Boss' has 420 pages → Python calls __str__
```

### What Dunder Methods Power

| Category | Triggered by | Common dunders |
|---|---|---|
| **Arithmetic** | `+`, `-`, `*`, `/` | `__add__`, `__sub__`, `__mul__`, `__truediv__` |
| **String behavior** | Concatenation, formatting, `str()` | `__add__`, `__format__`, `__str__`, `__repr__` |
| **Comparisons** | `==`, `<`, `>` | `__eq__`, `__lt__`, `__gt__` |
| **Iteration** | Looping over an object | `__iter__`, `__next__` |

> You never write `book1.__len__()` directly , you just write the natural Python expression (`len(book1)`), and the dunder method fires automatically underneath.

---

## Real-World Example: Shopping Cart

Let's combine everything into a practical, fully working class , a shopping cart that behaves like Python's built-in collections thanks to a handful of dunder methods.

```python
class Cart:
    def __init__(self):
        self.items = []  # every cart starts empty

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print(f'{item} is not in cart')

    def list_items(self):
        return self.items

    # --- Dunder methods bring built-in Python behavior to our custom class ---

    def __len__(self):
        return len(self.items)          # powers len(cart)

    def __getitem__(self, index):
        return self.items[index]        # powers cart[0], cart[1], etc.

    def __contains__(self, item):
        return item in self.items       # powers 'item' in cart

    def __iter__(self):
        return iter(self.items)         # powers for item in cart: ...
```

```python
cart = Cart()
cart.add('Laptop')

print(len(cart))        # 1      → thanks to __len__
print('Laptop' in cart) # True   → thanks to __contains__
```

**Why this matters:** because of those few dunder methods, `cart` now behaves like a native Python list in all the ways that count , you can check its length, search inside it, index into it, and loop over it , all using syntax you already know, instead of learning brand-new custom method names.

---

## Great Work!

You've just covered the foundation of Object-Oriented Programming in Python , the exact toolkit used to model real-world things in code, from users and products to game characters and bank accounts. Dunder methods in particular are what let your own custom classes feel just as natural to use as Python's built-in types. Keep experimenting , try building a class of your own! 

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
