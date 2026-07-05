# Graphs & Trees

> Networks, hierarchies, priority-based queues, and the specialized structures that power everything from GPS routing to autocomplete.

---

## Table of Contents

1. [Graphs Overview](#graphs-overview)
2. [Graph Traversals](#graph-traversals)
3. [Graph Representations](#graph-representations)
4. [Trees](#trees)
5. [Binary Trees & Binary Search Trees](#binary-trees--binary-search-trees)
6. [Tries](#tries)
7. [Priority Queues](#priority-queues)
8. [Heaps](#heaps)
9. [Python's heapq Module](#pythons-heapq-module)

---

## Graphs Overview

**Simple definition:** A graph is a set of nodes (also called vertices) connected by edges , together they form a network where nodes can link to multiple other nodes.

**Analogy:** A graph is like a map of flight routes between cities , each city is a node, and each direct flight is an edge connecting two of them. Some flights only go one way (directed), some routes loop back on themselves (cyclic), and some cities might have no flights connecting them to the rest of the map at all (disconnected).

### Types of Graphs

| Type | Meaning |
|---|---|
| **Directed** | Edges have a direction , like a one-way street (drawn with arrows) |
| **Undirected** | Edges have no direction , like a two-way street (simple lines) |
| **Cyclic** | Contains at least one cycle , a path that loops back to its starting node |
| **Acyclic (DAG)** | Contains no cycles at all , "Directed Acyclic Graph" |
| **Weighted** | Edges carry a value (e.g. distance, cost) usable in calculations |
| **Edge labeled** | Edges carry a descriptive label, drawn next to the edge |
| **Disconnected** | Some nodes have no path connecting them to others |

**Real-world uses:** maps and navigation, social networks, recommendation systems, and dependency resolution (like figuring out which software packages need to install before others).

---

## Graph Traversals

**Simple definition:** Traversal means visiting every node in a graph in some systematic order.

### Breadth-First Search (BFS)
**Simple definition:** BFS explores a graph **level by level**, checking all of a node's immediate neighbors before moving further out.

**Analogy:** BFS is like ripples spreading out from a stone dropped in a pond , it checks everything one "ring" away first, then the next ring out, and so on, always expanding outward evenly.

- Uses a **queue** (FIFO)
- Finds the **shortest path** in an unweighted graph

### Depth-First Search (DFS)
**Simple definition:** DFS dives as deep as possible down one path before backtracking to try another.

**Analogy:** DFS is like exploring a maze by picking a direction and following that single corridor as far as it goes , only turning back once you hit a dead end, rather than checking every nearby branch first.

- Uses a **stack** (or recursion)
- Great for **cycle detection** and general path-finding

| | BFS | DFS |
|---|---|---|
| **Structure used** | Queue | Stack (or recursion) |
| **Explores** | Level by level (outward) | One branch fully, then backtrack |
| **Best for** | Shortest path (unweighted) | Cycle detection, path existence |

---

## Graph Representations

**Analogy:** Think of these as two different ways to keep a friend list , a personal contact list per person (adjacency list) versus one giant "who knows who" spreadsheet with everyone listed against everyone else (adjacency matrix).

### Adjacency List
- Each node stores a list of just its own neighbors
- **Space-efficient** for sparse graphs (few connections relative to node count)
- Easy to loop through a node's neighbors directly

### Adjacency Matrix
- A 2D grid/array where both rows and columns represent nodes
- **Space-intensive** for large graphs (grows with the *square* of the node count)
- Very **fast** to check if a specific edge exists , just one direct lookup

---

## Trees

**Simple definition:** A tree is a special kind of graph that is both **acyclic** (no loops) and **connected** (every node is reachable from every other node).

**Analogy:** A tree is like a family tree or a company's org chart , everything branches downward from a single starting point, and there's no way to follow the branches back around into a loop.

**Key properties:**
- No cycles (no path leads back to where it started)
- Fully connected (nothing is isolated)

---

## Binary Trees & Binary Search Trees

### Binary Trees
**Simple definition:** A tree where each node has **at most two children** , commonly called the "left" and "right" child.

**Analogy:** Think of a knockout sports tournament bracket , each match (node) leads to, at most, two paths downward.

### Binary Search Trees (BST)
**Simple definition:** A binary tree with an extra rule: for every node, everything in its **left** subtree is smaller, and everything in its **right** subtree is larger.

**Analogy:** A BST is like a well-organized filing cabinet where, at every drawer, anything "smaller" always goes left and anything "bigger" always goes right , meaning you can find any file quickly by repeatedly choosing a direction, without checking every folder.

---

## Tries

**Simple definition:** A trie (also called a "prefix tree") is a tree structure specialized for storing strings, where each node represents a single character , and shared prefixes are stored only once.

**Analogy:** Think of a trie like a choose-your-own-adventure book of words , "CAT" and "CAR" would share the same first two pages (C, A) and only branch apart at the third letter. Instead of storing "CAT" and "CAR" as two totally separate entries, the shared beginning is written down just once.

**Why it's useful:** Perfect for autocomplete and spell-checking , related words naturally cluster together through shared prefixes.

**Complexity:** Search and insertion both run in `O(L)`, where `L` is the length of the string being searched or inserted , notably, this doesn't depend on how many other words are stored.

---

## Priority Queues

**Simple definition:** A priority queue is an abstract data type where each element carries a **priority** , and elements with higher priority get served first, no matter when they were added.

**Analogy:** A priority queue is like a hospital emergency room , patients aren't seen in the order they walked in (that would be a regular queue); the most critical cases get treated first, even if they arrived last.

| Structure | Serving order |
|---|---|
| **Queue** | First In, First Out (insertion order) |
| **Stack** | Last In, First Out (insertion order) |
| **Priority Queue** | Highest priority first (insertion order ignored) |

---

## Heaps

**Simple definition:** A heap is a specialized tree-based structure that keeps a strict ordering rule (the "heap property") between each parent node and its children , commonly used to power priority queues.

**Analogy:** A heap is like a company org chart where every manager must always have a "stronger" (or "weaker") stat than everyone reporting to them , instantly telling you who's at the very top, without needing to check every single employee.

### Max-Heap vs Min-Heap

| Type | Rule | Root contains |
|---|---|---|
| **Max-Heap** | Each parent ≥ its children | The **largest** element |
| **Min-Heap** | Each parent ≤ its children | The **smallest** element |

---

## Python's heapq Module

**Simple definition:** Python's built-in `heapq` module implements a **min-heap** using a regular list , giving you fast access to the smallest item at all times.

```python
import heapq

my_heap = []

# Insert elements one at a time
heapq.heappush(my_heap, 9)
heapq.heappush(my_heap, 3)
heapq.heappush(my_heap, 5)
print(my_heap)  # [3, 9, 5] → smallest is always at index 0

# Remove and return the smallest element
print(heapq.heappop(my_heap))  # 3
print(my_heap)                  # [5, 9]

# Push and pop in a single efficient step
print(heapq.heappushpop(my_heap, 7))  # 5 → pushes 7, then pops the smallest
print(my_heap)                         # [7, 9]

# Turn an existing list into a valid heap, in place
nums = [5, 7, 3, 1]
heapq.heapify(nums)
```

### Using Priorities with Tuples
**Trick:** Store `(priority, item)` tuples , Python's heap will automatically sort by the first value in each tuple, giving you priority-queue behavior for free.

```python
my_heap = []
heapq.heappush(my_heap, (3, "A"))
heapq.heappush(my_heap, (2, "B"))
heapq.heappush(my_heap, (1, "C"))

# Pops the lowest number first , i.e., the HIGHEST priority
print(heapq.heappop(my_heap))  # (1, "C")
```

> In this pattern, a **lower number = higher priority** , so if you want "priority 1" to genuinely mean "most urgent," this convention lines up perfectly with how `heapq` naturally pops the smallest value first.

---

## Excellent Work!

You've now covered some of the most powerful (and interview-favorite!) data structures in computer science , graphs for networks, trees for hierarchies, tries for string efficiency, and heaps for priority-based processing. These structures show up everywhere from GPS routing to task schedulers to search engines. 

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*