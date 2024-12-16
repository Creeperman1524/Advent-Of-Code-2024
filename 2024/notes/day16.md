# [Day 16 - Reindeer Maze](https://adventofcode.com/2024/day/16)

> [<- Previous](day15.md) | [Next ->](day17.md)

Truly the year of 2D grids, which sucks because this is where I feel I am lacking the most in writing algorithms. This can definitely be seen from how long it took me to
solve each part.

Still a neat problem, although pretty simplistic (in hindsight). Hope there are more logical puzzles coming up throughout the event!

|                | Part A  | Part B  |  Total  |
| -------------- | :-----: | :-----: | :-----: |
| Coding Time\*  | 1:29:30 | 2:37:13 | 4:06:43 |
| Execution Time | 0.175s  | 0.229s  | 0.404s  |

> \*Part B (and Total) are estimated as I went to sleep early and finsihed it later. They are based on self timing

## Part A

I really should be studying my graph algorithms, as it seems this advent is full of them. I knew from the initial maze that this will have to be some shortest path
algorithm. At first, I thought I'd implement [A\*](https://en.wikipedia.org/wiki/A*_search_algorithm), since I had already implemented a
[version of it before](https://github.com/Creeperman1524/SlidingPuzzleSolver/blob/e22669a7e5b04c44b85ada4c0ee59763d99723a4/slidingPuzzle.js#L48-L122).

However, I was struggling a lot in finding the correct implementation, so I decided to ditch the optimizations and go for another approach. (And I'm glad I did)

> [!TIP]
> You don't need to find the exact path of the maze, but rather the minimum scoring path of the maze. This can provide a lot of optimizations.

Using this trick, I decided to implement BFS with a priority queue. It will extend the search through each neighbor, always choosing to expand the neighbor
with the smallest score.

> [!NOTE]
> Each "neighbor" is technically not its true grid neighbor, as each tile can also be indexed with a rotation and it costs different amounts to turn. Therefore the
> states the BFS (and other algorithms) traverse through is not the true 2D maze.

It took me a while to think of (and code) this solution, so I defintely should remember to pre-write some algorithms or practice them more for next time!

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

    minCost = -1

    visited = set()
    queue = PriorityQueue()
    queue.put((0, s, 1))

    dirs = {1: (1, 0), 3: (-1, 0), 2: (0, 1), 0: (0, -1)}
    while not queue.empty():
        cost, (x, y), dir = queue.get()

        # Skip if we already saw this node
        if (x, y, dir) in visited:
            continue
        visited.add((x, y, dir))

        # Found the exit
        if maze[y][x] == "E":
            minCost = cost
            break

        # Continue straight
        dx, dy = dirs[dir]
        neighbor = maze[y + dy][x + dx]

        if neighbor != "#":
            queue.put((cost + 1, (x + dx, y + dy), dir))

        # Turn to other direcctions
        queue.put((cost + 1000, (x, y), (dir - 1) % 4))
        queue.put((cost + 1000, (x, y), (dir + 1) % 4))

    return minCost

```

## Part B

Oh boy sweet Part B, we meet again. Although a simple change, merely getting _all_ optimal paths and finding all the unique tiles it hits is way harder than it seems.

At first I wanted to try to the brute force approach. Finding _all_ possible paths from `S` to `E`, scoring them, taking the ones that score the least and counting all their unique tiles.
However, that process of getting _all_ possible paths is a pretty difficult one, and it led me down the rabbit hole of [P vs NP](https://en.wikipedia.org/wiki/P_versus_NP_problem),
[Yen's Algorithm](https://en.wikipedia.org/wiki/Yen%27s_algorithm), etc.

So I decided to take a break and head in for the night, making basically 0 progress for the first hour.

After getting up (and taking a final in the morning), I decided to work on the Part B some more and pivoted to using [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm),
as that is the more general case of A\* and I feel I will need the minimal path that it gives.

> [!TIP]
> Dijkstra's Algorithm worked very well here, as it gives the shortest score from any node to the start node. Using this, it can find a node on the minimal path and trace backwards.
> If two of its neighbors have the same score, then we found a branch in the minimal path (or 2 paths that still have the same minimal score)

Using this idea, I (very crudely) tried to find all previous nodes of the path which lead to the current node. This create a dictionary `fromNodes` which I can use to traverse again and find all nodes
calculate all "seats" on the best path.

> [!TIP]
> An issue I ran into was not discarding the previous nodes if a better path was found, leading to an overestimation of good seats on the final input.
>
> Funnily enough, this wasn't an issue for both test cases but became an issue on the actual input, leading me with false confidence and having no idea what went wrong.

Very convoluted, and definitely can be simplified with my spaghetti code, but it worked and I was very happy about that.

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
    costs[(s[0], s[1], 1)] = 0

    # Contains the best path(s) from that node back to the start node
    fromNodes = {}

    # A queue of neighbors to search next
    queue = PriorityQueue()
    queue.put((0, s, 1))

    # This can probably be simplified by prefilling all the dictionaries
    # so no checks are needed
    def calculateNodes(keyToAdd, key, cost, costModifier):
        if keyToAdd in costs:
            if costs[keyToAdd] > cost + costModifier:
                # Found better path for keyToAdd, update it's score
                costs[keyToAdd] = cost + costModifier

                # Remove all previous paths
                fromNodes[keyToAdd] = set()
                fromNodes[keyToAdd].add(key)
            if costs[keyToAdd] == cost + costModifier:
                # Adds the backwards node
                if keyToAdd in fromNodes:
                    fromNodes[keyToAdd].add(key)
                else:
                    fromNodes[keyToAdd] = set()
                    fromNodes[keyToAdd].add(key)

        else:
            costs[keyToAdd] = costs[key] + costModifier
            # Adds the backwards node
            if keyToAdd in fromNodes:
                fromNodes[keyToAdd].add(key)
            else:
                fromNodes[keyToAdd] = set()
                fromNodes[keyToAdd].add(key)

    # Performs Dijkstra's Algorithm to get the costs to each node
    dirs = {1: (1, 0), 3: (-1, 0), 2: (0, 1), 0: (0, -1)}
    while not queue.empty():
        cost, (x, y), dir = queue.get()
        key = (x, y, dir)

        # Skip if we already saw this node
        if key in visited:
            continue
        visited.add(key)

        # Found the exit
        if maze[y][x] == "E":
            break

        # Continue straight
        dx, dy = dirs[dir]
        neighbor = maze[y + dy][x + dx]

        if neighbor != "#":
            straightKey = (x + dx, y + dy, dir)
            queue.put((cost + 1, (x + dx, y + dy), dir))
            calculateNodes(straightKey, key, cost, 1)

        # Turn to other direcctions
        queue.put((cost + 1000, (x, y), (dir - 1) % 4))
        leftKey = (x, y, (dir - 1) % 4)
        calculateNodes(leftKey, key, cost, 1000)

        queue.put((cost + 1000, (x, y), (dir + 1) % 4))
        rightKey = (x, y, (dir + 1) % 4)
        calculateNodes(rightKey, key, cost, 1000)

    # costs[(e[0], e[1], 0)] contains the answer for Part A

    # Traverses the fromNodes backwards to find all best paths
    goodSeats = set()

    def dfs(fromNodes, currNode, s):
        for neighbor in fromNodes[currNode]:
            x, y, _ = neighbor

            goodSeats.add((x, y))
            if (x, y) == s:
                return

            dfs(fromNodes, neighbor, s)

        return

    goodSeats.add(e)
    dfs(fromNodes, (e[0], e[1], 0), s)

    return len(goodSeats)

```

