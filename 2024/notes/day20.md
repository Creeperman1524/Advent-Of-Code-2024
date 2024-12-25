# [Day 20 - Race Condition](https://adventofcode.com/2024/day/20)

> [<- Previous](day19.md) | [Next ->](day21.md)

Merry Christmas everyone! As I am a few days behind in completing these, I am currently writing this on Christmas!

As for this problem, we definitely have been getting a lot of 2D grid problems. They're fun, don't get me wrong, but I feel there should be a bit more variety.
It does help me because I get to reuse a lot of my code!

I took way too long on this problem for so many simple and stupid errors, I gotta fix that soon.

|                | Part A | Part B |  Total  |
| -------------- | :----: | :----: | :-----: |
| Coding Time\*  |        |        |         |
| Execution Time | 1.665s | 10.31s | 11.974s |

> \*Time is not recorded as this day was started on a different day. I intended to self time, but forgot. Both Part A and Part B took a bit of time though.

## Part A

This one started out pretty simple. I took the Dijkstra's Algorithm straight from [Day 16](day16.md), then using the costs and path generated to find the potential savings.

From there, went through each node in the path, went 2 out in each direction, and calculated the potential savings. I had many issues with bounds checking and the like, so
that's something I definitely should improve upon!

> [!TIP]
> An optimization could be to ignore creating the path (as I found out in Part B) as there is only 1 path and only the costs are needed.

```python
from queue import PriorityQueue


def solve(input):
    maze = []

    for line in input:
        maze.append(list(line))

    s = (0, 0)
    e = (0, 0)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "S":
                s = (x, y)
            if maze[y][x] == "E":
                e = (x, y)

    visited = set()
    # Contains the lowest cost found from the starting node to that node
    costs = {}
    # costs[(s[0], s[1])] = 0

    # A queue of neighbors to search next
    queue = PriorityQueue()
    queue.put((0, s))

    fromNodes = {}

    # Performs Dijkstra's Algorithm to get the costs to each node
    dirs = {(1, 0), (-1, 0), (0, 1), (0, -1)}
    while not queue.empty():
        cost, (x, y) = queue.get()
        key = (x, y)

        # Skip if we already saw this node
        if key in visited:
            continue
        visited.add(key)

        # Found the exit
        if maze[y][x] == "E":
            if key in costs:
                costs[key] = min(costs[key], cost)
            else:
                costs[key] = cost
            break

        for dx, dy in dirs:
            # Bounds checking
            if (
                x + dx < 0
                or x + dx > len(maze[y])
                or y + dy < 0
                or y + dy > len(maze)
                or maze[y + dy][x + dx] == "#"
                or (x + dx, y + dy) in visited
            ):
                continue

            queue.put((cost + 1, (x + dx, y + dy)))

            if key in costs:
                if costs[key] >= cost + 1:
                    costs[(x + dx, y + dy)] = cost + 1
                    fromNodes[(x + dx, y + dy)] = key
            else:
                costs[key] = cost + 1
                fromNodes[(x + dx, y + dy)] = key

    # Gets the final path
    path = []
    node = fromNodes[e]
    while node != s:
        path.append(node)
        node = fromNodes[node]
    path.append(s)

    # Find the max cost savings
    bigSavings = 0

    # Checks for a path to another node
    for node in path:
        x, y = node
        for dx, dy in dirs:
            newPos = (x + dx * 2, y + dy * 2)

            if newPos in path:
                savings = costs[node] - costs[newPos] - 2
                if savings >= 100:
                    bigSavings += 1

    return bigSavings

```

## Part B

This one really took me a long time. It was pretty simple to begin with, just search out at most 20 tiles rather than the hardcoded 2 tiles.

My first idea was to implement a depth-first search on _each node in the path_ to find all the other nodes it can reach (ignoring walls) within 20 moves or "picoseconds".
I soon realized this was a terrible idea and I should use a breadth-first search to expand out a diamond-shape (and get correct distance values)

After this not working for quite a while, I decided to sleep on it (into Christmas morning, haha). After taking that long break, I had a revelation on how to solve the problem.

> [!TIP]
> The problem states that it only wants to consider cheats that _land on a path tile within 20 moves_ (or how else are you going to continue from there?), and to also
> consider only unique cheats that are defined by their start and end.
>
> With this knowledge, I only needed to match up starts and ends to the cheats, rather than worrying about the tiles inbetween. I can easily find the distance using
> [Taxicab or Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry). I could simply loop through each pair of path nodes.

I still ran into many issues with my path missing nodes (which was giving me wrong values and causing such a headache). Eventually I resorted to ditching the path and
only using the nodes in the cost dict, which worked perfectly.

> [!TIP]
> This can definitely still be improved by potentially computing these "neighboring points within 20 taxicab distance" before, or something smart like that, but 10 seconds
> is still pretty good I feel

```python
from queue import PriorityQueue


def solve(input):
    maze = []

    for line in input:
        maze.append(list(line))

    s = (0, 0)
    e = (0, 0)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "S":
                s = (x, y)
            if maze[y][x] == "E":
                e = (x, y)

    visited = set()
    # Contains the lowest cost found from the starting node to that node
    costs = {}
    # costs[(s[0], s[1])] = 0

    # A queue of neighbors to search next
    queue = PriorityQueue()
    queue.put((0, s))

    # Performs Dijkstra's Algorithm to get the costs to each node
    dirs = {(1, 0), (-1, 0), (0, 1), (0, -1)}
    while not queue.empty():
        cost, (x, y) = queue.get()
        key = (x, y)

        # Skip if we already saw this node
        if key in visited:
            continue
        visited.add(key)

        # Found the exit
        if maze[y][x] == "E":
            costs[key] = cost + 1
            break

        for dx, dy in dirs:
            # Bounds checking
            if (
                x + dx < 0
                or x + dx > len(maze[y])
                or y + dy < 0
                or y + dy > len(maze)
                or maze[y + dy][x + dx] == "#"
                or (x + dx, y + dy) in visited
            ):
                continue

            queue.put((cost + 1, (x + dx, y + dy)))

            # Every node we hit will always be the min
            costs[key] = cost + 1

    # Find the max cost savings
    bigSavings = 0
    savingsArr = []

    for node in costs.keys():
        for otherNode in costs.keys():
            if node == otherNode:
                continue

            manhattanDistance = abs(node[0] - otherNode[0]) + abs(
                node[1] - otherNode[1]
            )
            if manhattanDistance > 20:
                continue

            savings = costs[otherNode] - costs[node] - manhattanDistance
            savingsArr.append(savings)

            if savings >= 100:
                bigSavings += 1

    return bigSavings

```

