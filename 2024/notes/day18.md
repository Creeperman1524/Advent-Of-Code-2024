# [Day 18 - RAM Run](https://adventofcode.com/2024/day/18)

> [<- Previous](day17.md) | [Next ->](day19.md)

This one was a nice breath of fresh air after all of the difficult problems for the past few days. If I was going for speed, I definitely could've finished this much quicker with
some dirty code, but I am very happy about it.

|                    | Part A | Part B  |  Total  |
| ------------------ | :----: | :-----: | :-----: |
| Coding Time        | 21:23  |  16:09  |  37:32  |
| Execution Time     | 0.138s | 11.660s | 11.798s |
| Addendum Exec Time | 0.138s | 5.856s  | 5.993s  |

## Part A

A very simplistic problem. First, calculate (with some hardcoded values, I hate when they make us do this) the blockers that fall onto the memory. Then traverse the memory map, avoiding
the blockers and find the minimum amount of steps needed to get to the bottom right.

I actually yoinked my modified A\* code from [Day 16](day16.md), which was nice to not have to type all of that again. Is this the power of having helpful util modules? It was
also nice to not need to mess around with grids, as all information can be tracked through coordinates rather than a 2D array.

Pretty straight forward though, although I did forget to do some bounds checking and had the escpae route walking _around the outside of the map_, which was giving me a lower-than-expected
answer. Pretty funny.

```python
from queue import PriorityQueue


def solve(input):
    size = 71
    fallen = 1024

    blockers = []

    for line in input:
        # Only calculate the amount needed
        if fallen <= 0:
            break
        x, y = list(map(int, line.split(",")))
        blockers.append((x, y))
        fallen -= 1

    minSteps = 0

    visited = set()
    queue = PriorityQueue()
    queue.put((0, (0, 0)))

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while not queue.empty():
        steps, (x, y) = queue.get()

        # Skip if we already saw this node
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Found the exit
        if x == size - 1 and y == size - 1:
            minSteps = steps
            break

        # Add neighbors
        for dx, dy in dirs:
            if (x + dx) < 0 or (x + dx) >= size or (y + dy) < 0 or (y + dy) >= size:
                continue

            if (x + dx, y + dy) not in blockers:
                queue.put((steps + 1, (x + dx, y + dy)))

    return minSteps

```

## Part B

Brute force, oh how I missed you!! I seriously thought they were setting up the problem to _solve the maze while the corrupted bytes were falling_, which definitely would've been
an interesting one. But nope, we only have to find the byte that first blocks the path to the exit.

After looking through the input, it only consisted of `3450 lines/bytes`, meaning the search space was pretty small so brute forcing could definitely work given enough patience.

I initiallized just moved all the search logic into the parsing logic and returned the last blocker placed when a path can no longer be found. This worked fine and all, but after doing
some debugging prints it was just going too slow for my liking (hindsight, it definitely could've finished within ~1 minute or so).

> [!TIP]
> My first idea for a speedup was _only to recalculate the escape path if a blocker lands on it_. Now this required more logic to save the path rather than the steps taken, but after
> much practice from the other days I implemented it with ease. This helped immensely and allowed the program to parse through most of the input within ~10 seconds! Hooray!

And that's it! I waited around for a bit while cleaning up my code and bam, another day completed.

> [!TIP]
> An even cooler trick is to add all bytes to 1024 to begin with, as Part A already guarantees it to contain a safe path. Maybe I'll add this in the Addendum for a small speedup.

```python
from queue import PriorityQueue


def solve(input):
    size = 71

    blockers = []
    bestPath = []

    for line in input:
        bx, by = list(map(int, line.split(",")))
        blockers.append((bx, by))

        # Skip simulating new paths for blockers that do not fall on the current path
        if (bx, by) not in bestPath and len(bestPath) > 0:
            continue

        visited = set()
        queue = PriorityQueue()
        queue.put((0, (0, 0)))
        pathDict = {}

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        escaped = False
        while not queue.empty():
            steps, (x, y) = queue.get()

            # Skip if we already saw this node
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Found the exit
            if x == size - 1 and y == size - 1:
                escaped = True
                break

            # Add neighbors
            for dx, dy in dirs:
                if (x + dx) < 0 or (x + dx) >= size or (y + dy) < 0 or (y + dy) >= size:
                    continue

                if (x + dx, y + dy) not in blockers and (x + dx, y + dy) not in visited:
                    queue.put((steps + 1, (x + dx, y + dy)))
                    pathDict[(x + dx, y + dy)] = (x, y)

        if escaped:
            # Save the new path after a blocker appeared on it
            bestPath.clear()
            node = (size - 1, size - 1)
            while node != (0, 0):
                bestPath.append(node)
                node = pathDict[node]

            bestPath.append

        else:
            # Return the blocker that first stopped our path
            return (bx, by)

    return "Always possible"

```

### Addendum (12/18/24)

As mentioned above, this small edit only starts calculating paths after 1024 bytes have been released.
This provides a `2x` speedup from `11.660s` to `5.856s`, as it drastically reduces the search space needed for the problem.

There are also some small readability changes when checking for neighbors.

> [!NOTE]
> Now this is beginning to borderline "just print the correct answer after getting it separately, duh" from the hardcoding being done, but I'll allow this since any input
> will also need to pass Part A, meaning this technique is valid for all puzzle inputs.

```python
from queue import PriorityQueue


def solve(input):
    size = 71

    blockers = []
    bestPath = []
    counter = 0

    for line in input:
        counter += 1
        bx, by = list(map(int, line.split(",")))
        blockers.append((bx, by))

        # Part A guarantees bytes up to 1024 have a safe path
        if counter < 1024:
            continue

        # Skip simulating new paths for blockers that do not fall on the current path
        if (bx, by) not in bestPath and len(bestPath) > 0:
            continue

        # Calculate the best path given the blockers
        visited = set()
        queue = PriorityQueue()
        queue.put((0, (0, 0)))
        pathDict = {}

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        escaped = False
        while not queue.empty():
            steps, (x, y) = queue.get()

            # Skip if we already saw this node
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Found the exit
            if x == size - 1 and y == size - 1:
                escaped = True
                break

            # Add neighbors
            for dx, dy in dirs:
                newX, newY = x + dx, y + dy
                if (
                    not (0 < newX < size)
                    or not (0 < newY < size)
                    or (newX, newY) in blockers
                    or (newX, newY) in visited
                ):
                    continue

                queue.put((steps + 1, (newX, newY)))
                pathDict[(newX, newY)] = (x, y)

        if escaped:
            # Save the new path after a blocker appeared on it
            bestPath.clear()
            node = (size - 1, size - 1)
            while node != (0, 0):
                bestPath.append(node)
                node = pathDict[node]

            bestPath.append

        else:
            # Return the blocker that first stopped our path
            return (bx, by)

    return "Always possible"

```

