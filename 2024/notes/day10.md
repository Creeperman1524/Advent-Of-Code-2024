# [Day 10 - Hoof It](https://adventofcode.com/2024/day/10)

> [<- Previous](day09.md) | [Next ->](day11.md)

Man I'm disappointed in myself for this one. Definitely need to brush up on my algorithms as this was as simple as it can get with
DFS and BFS. I also spent too much time debugging only to realize python is weird with it's global variables (or maybe my `grader.py`
script is doing something funky).

Overall pretty easy problem, could have been done way faster if I wasn't so tired and had practice!

|                | Part A | Part B | Total  |
| -------------- | :----: | :----: | :----: |
| Coding Time    | 43:05  |  6:32  | 49:37  |
| Execution Time | 0.002s | 0.002s | 0.003s |

## Part A

Just a simple DFS for each direction the trail could possible go in, and tallying up which actually complete the journey.

My mistake here was making the `visited` set in the global scope. Even though I was calling `visited = set()` within the loop, it still was having
a weird interaction and didn't seem to be clearing itself between test cases. This most likely wouldn't have been an issue but it seemed to bug out with my `grader.py` script.

Although, this solution is much cleaner compared to what I was hacking together before, so I am satisfied.

```python
def solve(input):
    scores = 0
    visited = set()

    grid = []

    # Parses the grid
    for line in input:
        grid.append(list(map(int, line)))

    # Run a search on all 0s
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:

                visited.clear()
                score = search(grid, x, y, visited)
                scores += score

    return scores


# A search from a 0 to all reachable 9s
def search(grid, x, y, visited):
    if (x, y) in visited:
        return 0

    visited.add((x, y))

    elem = grid[y][x]
    if elem == 9:
        return 1

    score = 0

    # Up
    if y > 0 and grid[y - 1][x] == elem + 1:
        score += search(grid, x, y - 1, visited)

    # Down
    if y < len(grid) - 1 and grid[y + 1][x] == elem + 1:
        score += search(grid, x, y + 1, visited)

    # Left
    if x > 0 and grid[y][x - 1] == elem + 1:
        score += search(grid, x - 1, y, visited)

    # Right
    if x < len(grid[0]) - 1 and grid[y][x + 1] == elem + 1:
        score += search(grid, x + 1, y, visited)

    return score

```

## Part B

Literally exactly the same as Part A, except it no longer keeps track of visited nodes. ~~I think I might have lucked out here and not
had any loops in my input, so this could potentially break with the wrong input.~~ After thinking about it more, there is no possible way for the
trails to loop, as they always must be increasing so no loop could form.

I definitely should do a deeper dive into how this code words, as I more-or-less just ripped out the visited nodes stuff and prayed it work
(for reasons I definitely cannot explain)

```python
def solve(input):
    scores = 0

    grid = []

    # Parses the grid
    for line in input:
        grid.append(list(map(int, line)))

    # Run a search on all 0s
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:

                score = search(grid, x, y)
                scores += score

    return scores


# A search from a 0 to all reachable 9s
def search(grid, x, y):
    elem = grid[y][x]
    if elem == 9:
        return 1

    score = 0

    # Up
    if y > 0 and grid[y - 1][x] == elem + 1:
        score += search(grid, x, y - 1)

    # Down
    if y < len(grid) - 1 and grid[y + 1][x] == elem + 1:
        score += search(grid, x, y + 1)

    # Left
    if x > 0 and grid[y][x - 1] == elem + 1:
        score += search(grid, x - 1, y)

    # Right
    if x < len(grid[0]) - 1 and grid[y][x + 1] == elem + 1:
        score += search(grid, x + 1, y)

    return score

```
