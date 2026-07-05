# Installing Python

> Everything you need to get Python running on your own machine, explained simply.

---

## Table of Contents

1. [Installing Python](#installing-python)
2. [What is a Terminal?](#what-is-a-terminal)
3. [What is an IDE?](#what-is-an-ide)
4. [Popular Code Editors](#popular-code-editors)
5. [Running Code Locally](#running-code-locally)
6. [The Python Interactive Shell](#the-python-interactive-shell)
7. [The REPL Cycle](#the-repl-cycle)

---

## Installing Python

**Simple definition:** Installing Python means downloading the official Python program onto your computer so it can understand and run `.py` files.

**Analogy:** Installing Python is like installing a translator app before visiting a foreign country , without it, your computer has no idea what to do with the "language" you're writing in.

**How to do it:**
- Go to **[python.org](https://www.python.org/)**
- Hover over **"Downloads"**
- Click the button showing the current version for your OS (Windows, Mac, or Linux)
- Run the installer and follow the prompts

> **Windows users:** During install, make sure to check **"Add python.exe to PATH"** , this saves you a headache later, since it lets you run `python` from any folder in your terminal.

**Verify it worked** by opening your terminal and typing:

```bash
python --version
# or, on some systems:
python3 --version
```

If you see something like `Python 3.12.2`, you're good to go!

> **Heads up:** On some older Mac/Linux systems, `python` might point to the outdated Python 2 (end-of-life, don't use it for new projects). If `python --version` shows `Python 2.x.x`, just use `python3` instead going forward.

---

## What is a Terminal?

**Simple definition:** A terminal is a text-based way to talk to your computer , instead of clicking icons, you type commands.

**Analogy:** If your desktop with icons and windows is like ordering food by pointing at pictures on a menu, the terminal is like calling in your order directly , more direct, a little intimidating at first, but way faster once you know the "menu" (commands).

| OS | Default Terminal App |
|---|---|
| macOS | Terminal |
| Windows | Command Prompt or PowerShell |
| Linux | Depends on desktop , e.g. GNOME Terminal, Konsole |

---

## What is an IDE?

**Simple definition:** IDE stands for **Integrated Development Environment** , a single app that bundles the tools you need to write, test, and run code.

**Analogy:** An IDE is like a fully-stocked workshop instead of a single toolbox , you've got your code editor, a built-in terminal, and testing tools all in one place, instead of switching between separate apps.

---

## Popular Code Editors

Some go-to choices for Python development:

- **VS Code** , free, lightweight, hugely popular ([download here](https://code.visualstudio.com/download))
- **PyCharm** , feature-rich, Python-specific IDE
- **Spyder** , popular in the data science community

---

## Running Code Locally

**Simple definition:** "Running code locally" just means executing your Python file on your own computer, rather than in an online editor.

**Analogy:** It's the difference between practicing piano on a keyboard at a music store (an online editor) versus on your own piano at home (your local machine) , same skill, but now it's set up permanently in your own space.

**Option 1 , The Run button:**
In VS Code, click the play button in the upper-right corner. This opens a terminal automatically and runs your script.

**Option 2 , Run it manually from the terminal:**

```bash
# Step 1: Navigate into the folder containing your file
cd python-projects

# Step 2: Run the file
python main.py
```

> If `python main.py` doesn't work, try `python3 main.py` , common on macOS/Linux setups where both Python 2 and 3 exist.

---

## The Python Interactive Shell

**Simple definition:** The interactive shell is a mode where you type one line of Python at a time and see the result immediately , no need to save a whole file first.

**Analogy:** Think of it like a chat conversation with Python , you say something, it replies instantly, then waits for your next line. A full `.py` script, by contrast, is more like mailing a whole letter and waiting for one final response.

**How to open it:** Type `python` (or `python3`) in your terminal and press **Enter**. You'll see something like:

```bash
Python 3.12.2 (main, Mar 21 2024, 22:48:26) [Clang 14.0.3] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

That `>>>` is Python's way of saying *"I'm listening , type something."*

```bash
>>> print("Hello, world!")
Hello, world!
>>>
```

**To exit:** type `exit()`, or press `Ctrl + D` (Mac/Linux) / `Ctrl + Z` then `Enter` (Windows).

> **When to use it:** Great for quick experiments and testing small snippets. For anything longer or multi-file, stick to a code editor.

---

## The REPL Cycle

**Simple definition:** REPL stands for **Read, Evaluate, Print, Loop** , it's the exact process the interactive shell follows every time you hit Enter.

**Analogy:** Picture a conversation loop with a very literal assistant: they **R**ead what you said, **E**valuate what it means, **P**rint their response, then **L**oop back and wait to hear from you again , over and over, forever (until you say goodbye).

```bash
>>> something random
  File "<stdin>", line 1
    something random
              ^^^^^^
SyntaxError: invalid syntax
```

Even when you type something invalid, the REPL still completes its cycle , it just prints an error instead of a result, then loops back to `>>>` for your next attempt. Errors here are totally normal , it's Python's way of pointing out a typo, not a sign something's broken.

---

## You're Set Up!

You now know how to install Python, open a terminal, choose an editor, and run code both as full scripts and one line at a time. From here, every lesson you go through can (and should!) be tested on your own machine , that's where the real learning sticks.

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*