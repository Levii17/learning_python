# Dynamic Programming — The Beginner-Friendly Guide

> Turning painfully slow recursive problems into fast, efficient solutions by remembering what you've already solved.

---

## Table of Contents

1. [What is Dynamic Programming?](#-what-is-dynamic-programming)
2. [Core Principles](#-core-principles)
3. [The Problem with Naive Recursion](#-the-problem-with-naive-recursion)
4. [Memoization (Top-Down)](#-memoization-top-down)
5. [Tabulation (Bottom-Up)](#-tabulation-bottom-up)
6. [Space-Optimized Tabulation](#-space-optimized-tabulation)
7. [Practical Example: Coin Change Problem](#-practical-example-coin-change-problem)
8. [Real-World Applications](#-real-world-applications)
9. [When to Use Dynamic Programming](#-when-to-use-dynamic-programming)

---

## What is Dynamic Programming?

**Simple definition:** Dynamic programming (DP) is a technique for solving complex problems by breaking them into simpler subproblems, and — crucially — **storing** the results so you never solve the same subproblem twice.

**Analogy:** Imagine doing your times tables homework, and every time you need `7 × 8`, you re-derive it from scratch by adding 7 eight times. Dynamic programming is like writing that answer down the first time you calculate it, then just glancing at your notes every time it comes up again — the math doesn't change, so why redo the work?

DP can take problems that would normally take **exponential time** and shrink them down to **polynomial time** — often the difference between a program finishing instantly versus one that would still be running years from now.

---

## Core Principles

Dynamic programming applies when a problem has **both** of these properties:

### 1. Overlapping Subproblems
**Simple definition:** The same smaller calculation gets requested again and again while solving the bigger problem.

**Analogy:** Like multiple recipes in a cookbook all separately calling for "prepare a basic tomato sauce" — instead of making that sauce from scratch every single time, you make a big batch once and reuse it wherever it's needed.

### 2. Optimal Substructure
**Simple definition:** The best overall solution can be built directly from the best solutions to its smaller pieces.

**Analogy:** Like planning the cheapest possible road trip — if you know the cheapest route from City A to City B, and the cheapest route from City B to City C, the cheapest full trip A→C is just those two best routes combined.

---

## The Problem with Naive Recursion

Let's look at the classic **"climbing stairs"** problem: you're climbing a staircase of `n` steps, and can move up either 1 or 2 steps at a time. How many distinct ways can you reach the top?

```python
def climb_stairs_recursive(n):
    if n <= 2:
        return n  # base cases: 1 way for 1 step, 2 ways for 2 steps
    # To reach step n, you could have come from step (n-1) or step (n-2)
    return climb_stairs_recursive(n-1) + climb_stairs_recursive(n-2)
```

**The problem:** this recalculates the same values over and over. For `climb_stairs(5)`:
- `climb_stairs(5)` calls `climb_stairs(4)` and `climb_stairs(3)`
- `climb_stairs(4)` *also* calls `climb_stairs(3)` — a repeat!
- `climb_stairs(3)` gets calculated twice, `climb_stairs(2)` gets calculated three times total

For `n=5`, that's **9 function calls** to get just **5 unique answers**. As `n` grows, this redundancy explodes — `climb_stairs(30)` would trigger *millions* of calls.

> This naive approach runs in `O(2ⁿ)` time — exponential, and impractical for anything beyond small inputs.

---

## Memoization (Top-Down)

**Simple definition:** Memoization solves the problem exactly like the recursive version above, but **caches** each result the first time it's calculated — so repeat calls become an instant lookup instead of more recursion.

**Analogy:** It's like keeping sticky notes on your desk with answers you've already worked out — next time the same question comes up, you just glance at the note instead of solving it all over again.

```python
def climb_stairs_memo(n, memo={}):
    if n in memo:
        return memo[n]  # cached result — instant O(1) lookup!

    if n <= 2:
        return n

    memo[n] = climb_stairs_memo(n-1, memo) + climb_stairs_memo(n-2, memo)
    return memo[n]
```

### Tracing climb_stairs_memo(5)
```
Call: climb_stairs_memo(5)

  Call: climb_stairs_memo(4)

    Call: climb_stairs_memo(3)
      Call: climb_stairs_memo(2) → returns 2 (base case)
      Call: climb_stairs_memo(1) → returns 1 (base case)
      Result: 2 + 1 = 3
      memo = {3: 3}   ← stored!

    Call: climb_stairs_memo(2) → returns 2 (base case)
    Result: 3 + 2 = 5
    memo = {3: 3, 4: 5}   ← stored!

  Call: climb_stairs_memo(3) → returns 3 FROM MEMO — no recursion needed!

  Result: 5 + 3 = 8
  memo = {3: 3, 4: 5, 5: 8}
```

Notice `climb_stairs_memo(3)` only ever gets *calculated* once — the second time it's needed, it's just a dictionary lookup.

**Efficiency comparison:**
| | Naive Recursion | Memoization |
|---|---|---|
| Function calls for n=5 | 9 (with repeats) | 5 unique calculations |
| Time Complexity | `O(2ⁿ)` | `O(n)` |
| Space Complexity | `O(n)` (call stack) | `O(n)` (memo + call stack) |
| n=30 in practice | Millions of calls | ~30 calculations |

---

## Tabulation (Bottom-Up)

**Simple definition:** Tabulation flips the approach — instead of starting big and recursing down, it starts from the smallest subproblem and iteratively **builds up** to the final answer, filling in a table (array) along the way.

**Analogy:** If memoization is like solving a big question and jotting down answers to sub-questions as you stumble into them, tabulation is like methodically filling in a crossword puzzle starting from square 1 — no backtracking, just steady forward progress.

```python
def climb_stairs_tabulation(n):
    if n <= 2:
        return n

    dp = [0] * (n + 1)  # table to store results for steps 0 through n
    dp[1] = 1  # 1 way to reach step 1
    dp[2] = 2  # 2 ways to reach step 2

    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]  # build on the two previous results

    return dp[n]
```

### Watching the table fill in for climb_stairs(5)
```
Initial:
dp = [0, 1, 2, 0, 0, 0]
      0  1  2  3  4  5   ← index (step number)

i = 3:  dp[3] = dp[2] + dp[1] = 2 + 1 = 3   → dp = [0,1,2,3,0,0]
i = 4:  dp[4] = dp[3] + dp[2] = 3 + 2 = 5   → dp = [0,1,2,3,5,0]
i = 5:  dp[5] = dp[4] + dp[3] = 5 + 3 = 8   → dp = [0,1,2,3,5,8]

Final result: dp[5] = 8
```

### Why Tabulation Has Advantages Too
- **No recursion overhead** — no risk of hitting Python's recursion limit on huge inputs
- **Predictable execution order** — always calculated in a clean 1, 2, 3... sequence
- **Cache-friendly** — sequential array access tends to be faster at the hardware level

---

## ⚡ Space-Optimized Tabulation

**Simple definition:** Since each step only ever needs the *previous two* values, we don't actually need to keep the whole table — just two rolling variables.

```python
def climb_stairs_optimized(n):
    if n <= 2:
        return n

    prev2, prev1 = 1, 2  # only track the last two results
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1
```

This shrinks space complexity from `O(n)` down to `O(1)` — same speed, far less memory.

**Overall efficiency comparison:**
| | Naive Recursion | Tabulation |
|---|---|---|
| Time Complexity | `O(2ⁿ)` | `O(n)` |
| Space Complexity | `O(n)` call stack | `O(n)`, or `O(1)` optimized |
| Stack overflow risk | High for large n | None |

---

## Practical Example: Coin Change Problem

**The question:** What's the *minimum* number of coins needed to make a target amount, given a set of coin denominations?

This problem beautifully demonstrates both DP principles: **overlapping subproblems** (the same smaller amounts get reused constantly) and **optimal substructure** (the best way to make a big amount builds directly on the best way to make smaller amounts).

```python
def min_coins(amount, coins):
    dp = [float('inf')] * (amount + 1)  # start assuming every amount is "impossible"
    dp[0] = 0  # base case: 0 coins needed to make amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:  # only usable if it doesn't exceed the current amount
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### Walking Through coins = [1, 3, 4], amount = 6
```
Initial:
dp = [0, ∞, ∞, ∞, ∞, ∞, ∞]
      0  1  2  3  4  5  6   ← amounts

amount 1: dp[1] = dp[0]+1 = 1              → dp = [0,1,∞,∞,∞,∞,∞]
amount 2: dp[2] = dp[1]+1 = 2              → dp = [0,1,2,∞,∞,∞,∞]
amount 3: dp[3] = min(dp[2]+1, dp[0]+1) = 1 → dp = [0,1,2,1,∞,∞,∞]
amount 4: dp[4] = min(..., dp[0]+1) = 1     → dp = [0,1,2,1,1,∞,∞]
amount 5: dp[5] = min(..., dp[1]+1) = 2     → dp = [0,1,2,1,1,2,∞]
amount 6: dp[6] = min(dp[3]+1, dp[2]+1) = 2 → dp = [0,1,2,1,1,2,2]

Final: dp[6] = 2   (achieved with 3 + 3)
```

**Why this matters:** without DP, you'd need to test every possible *combination* of coins — an exponential explosion of possibilities. With DP, each amount from 1 to 6 is solved exactly once, and every larger amount reuses the smaller answers already stored.

**Complexity:**
- **Time:** `O(amount × number of coin types)` — dramatically better than trying every combination
- **Space:** `O(amount)` for the `dp` array

---

## Real-World Applications

- **Route Optimization** — GPS systems use DP-based algorithms to compute shortest paths
- **Text Processing** — spell checkers and autocomplete use DP to calculate "edit distance" between words
- **Financial Modeling** — investment and portfolio optimization strategies
- **Resource Allocation** — the classic "knapsack problem" and its variants appear in scheduling and budgeting

---

## When to Use Dynamic Programming

Reach for DP when:
- The problem breaks down into **overlapping subproblems**
- The problem shows **optimal substructure**
- A naive recursive approach would involve heavy repeated calculations
- You're willing to trade a bit of **extra memory** for a **big speed boost**

**Common DP problem patterns:**
- **Optimization problems** — finding a minimum or maximum value
- **Counting problems** — counting the number of ways to achieve something
- **Decision problems** — breaking a choice down into smaller sequential choices

---

## Fantastic Progress!

Dynamic programming is one of the most powerful — and most feared! — topics in computer science, but at its core it's just one simple idea: don't redo work you've already done. Once "overlapping subproblems" and "optimal substructure" start jumping out at you in new problems, you'll have unlocked one of the most valuable problem-solving tools in all of programming.

---
*Notes compiled and designed by [@x_mxolisi_x](https://instagram.com/x_mxolisi_x)*
