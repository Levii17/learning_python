# Searching & Sorting Algorithms

> Two searching strategies and one powerful sorting technique , with the "why" behind their efficiency.

---

## Table of Contents

1. [Linear Search](#-linear-search)
2. [Binary Search](#-binary-search)
3. [Linear Search vs Binary Search](#-linear-search-vs-binary-search)
4. [Divide and Conquer](#-divide-and-conquer)
5. [Merge Sort](#-merge-sort)

---

## Linear Search

**Simple definition:** Linear search checks every item in a list, one at a time from the very start, until it finds the target , or runs out of items to check.

**Analogy:** Linear search is like looking for your friend's name in a phone book by starting on page one and reading every single entry in order , reliable, but slow if the name happens to be near the end.

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i   # found it! return the index
    return -1           # never found , -1 signals "not in the list"
```

```python
numbers = [13, 4, 7, 9, 10]

linear_search(numbers, 9)  # 3  → 9 is at index 3
linear_search(numbers, 5)  # -1 → 5 isn't in the list at all
```

> **Why -1?** It's not a valid index in most languages, so it works as a clear "not found" signal that could never be confused with a real position in the list.

**Complexity:**
- **Time:** `O(n)` , worst case, you check every single item once
- **Space:** `O(1)` , no extra memory needed, just a running check

---

## Binary Search

**Simple definition:** Binary search repeatedly cuts a **sorted** list in half, checking the middle item and eliminating the half that can't contain the target , dramatically reducing how many items you need to check.

**Analogy:** Binary search is like looking up a name in a *paper* phone book the smart way , you flip open to the middle, see whether your name comes before or after that point alphabetically, then throw away the half you don't need and repeat. You'd never need to read every single page.

> **The catch:** Binary search only works on a list that's already **sorted**. If your data isn't sorted, binary search's "which half do I ignore?" logic falls apart.

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2  # the middle index of the current range

        if arr[mid] == target:
            return mid            # found it!
        elif arr[mid] < target:
            low = mid + 1         # target must be in the RIGHT half
        else:
            high = mid - 1        # target must be in the LEFT half

    return -1  # search range shrank to nothing , target isn't in the list
```

**Walking through the logic:**
1. Set a `low` and `high` boundary , the range you're currently searching
2. While that range is still valid (`low <= high`), check the middle item
3. Exact match? Return its index immediately
4. Middle value too small? The target must be to the right , move `low` up
5. Middle value too big? The target must be to the left , move `high` down
6. Repeat until found, or the range collapses (meaning it's not in the list)

**Complexity:**
- **Time:** `O(log n)` , the search space is cut in half every single step
- **Space:** `O(1)` , no extra memory needed

---

## Linear Search vs Binary Search

| | Linear Search | Binary Search |
|---|---|---|
| **Requires sorted data?** | No | Yes |
| **Time Complexity** | `O(n)` | `O(log n)` |
| **Space Complexity** | `O(1)` | `O(1)` |
| **Best for** | Small or unsorted lists | Large, sorted lists |

> **Rule of thumb:** If your data is already sorted and might be large, binary search will vastly outperform linear search as the list grows. If your data isn't sorted (and sorting it isn't worth the cost for a one-off search), linear search is simpler and gets the job done.

---

## Divide and Conquer

**Simple definition:** Divide and conquer is a strategy for solving a big problem by breaking it into smaller, more manageable sub-problems, solving each one, then combining the results.

**Analogy:** Think of divide and conquer like organizing a massive, messy garage , instead of tackling the whole room at once, you split it into small piles (tools, boxes, sports gear), sort each small pile individually (much easier!), then bring the organized piles back together into one tidy garage.

**Recursion** is the technique that usually powers this , a function that calls itself repeatedly on smaller and smaller pieces of the problem, until it hits a "base case" simple enough to solve directly (like a pile of just one item, which is already "sorted" by definition).

---

## Merge Sort

**Simple definition:** Merge sort is a sorting algorithm that recursively splits a list in half until each piece has just one element, then merges those pieces back together in sorted order.

**Analogy:** Imagine sorting a deck of cards by first splitting it into two piles, splitting each of those into two more piles, and so on , until you're just holding individual cards (which are trivially "sorted" on their own). Then you merge pairs of piles back together, always placing the smaller card first, until you're holding one fully sorted deck again.

### Step-by-Step Walkthrough
Starting list: `42 37 53 17`

**1. Split in half:**
```
42 37  |  53 17
```

**2. Keep splitting the left side until each piece has 1 item:**
```
42  |  37
```
A single item is automatically "sorted" , nothing to compare it to.

**3. Merge those single items back together, in order:**
```
37 42
```

**4. Do the same for the right side:**
```
53 | 17   →  merge in order  →   17 53
```

**5. Merge the two now-sorted halves together:**
```
17 37 42 53
```

### The Code
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr  # base case: a list of 0 or 1 items is already sorted

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # recursively sort the left half
    right = merge_sort(arr[mid:])  # recursively sort the right half

    # Merge the two sorted halves back together
    sorted_list = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    # Add on any leftover items (one side always finishes first)
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])

    return sorted_list
```

**Complexity:**
- **Time:** `O(n log n)` , the list gets divided in half repeatedly (`log n` levels), and merging all the pieces back together at each level costs `O(n)`
- **Space:** `O(n)` , unlike some sorting algorithms (like bubble sort), merge sort isn't "in-place" , it builds new lists as it merges, so it needs extra memory proportional to the input size

---

## Great Progress!

You now understand two fundamentally different ways to search data, plus the divide-and-conquer thinking that powers some of the most efficient sorting algorithms out there. These concepts show up constantly , not just in interviews, but any time you're deciding how to structure and search through real data efficiently. 

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
