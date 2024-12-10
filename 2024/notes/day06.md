# [Day 6 - Guard Galivant](https://adventofcode.com/2024/day/6)

> [<- Previous](day05.md) | [Next ->](day07.md)

Ah, isn't it the consequences of my own (brute forcing) actions. Although in the private leaderboard I am in, we discussed
what seems to be the correct (optimal) solution for Part 2 and can't seem to come to an agreement.

This still was a very fun problem, and I almost thought it was going to be one of those puzzle games where you have to push the cubes!

|                | Part A | Part B  |  Total  |
| -------------- | :----: | :-----: | :-----: |
| Coding Time    | 31:13  |  16:20  |  47:33  |
| Execution Time | 0.002s | 20.846s | 20.848s |

## Part A

The difficulty I had with this part was moving the guard around the grid. As explained through the other days
of this, having better helper functions (especially those dealing with grids) would have done wonders here.

Other than that, I simply followed the instructions of the prompt, have the guard turn right each time they bump
into an obstacle and keep track of all the unique tiles they visited.

```python
def solve(input):
    grid = []
    tiles = set()

    # Parses the grid
    for line in input:
        grid.append(list(line))

    guardx = 0
    guardy = 0
    facing = "up"

    # Finds the guard
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "^":
                guardx = x
                guardy = y

    # While the guard is in bounds
    while not (
        (guardx <= 0 and facing == "left")
        or (guardx >= len(grid[0]) - 1 and facing == "right")
        or (guardy <= 0 and facing == "up")
        or (guardy >= len(grid) - 1 and facing == "down")
    ):
        if facing == "up":
            guardy -= 1
            if grid[guardy][guardx] == "#":
                facing = "right"
                guardy += 1
                continue
            tiles.add((guardx, guardy))
        elif facing == "right":
            guardx += 1
            if grid[guardy][guardx] == "#":
                facing = "down"
                guardx -= 1
                continue
            tiles.add((guardx, guardy))
        elif facing == "down":
            guardy += 1
            if grid[guardy][guardx] == "#":
                facing = "left"
                guardy -= 1
                continue
            tiles.add((guardx, guardy))
        elif facing == "left":
            guardx -= 1
            if grid[guardy][guardx] == "#":
                facing = "up"
                guardx += 1
                continue
            tiles.add((guardx, guardy))

    return len(tiles)

```

## Part B

Back at it again with brute force, aw yeah. Although I do feel I was pretty smart about how I went about it.

> [!TIP]
>
> 1. The obstacle _must_ be in the current path of the guard, or else they would never hit it to create a cycle.
> 2. The guard must be on a tile and facing in the same direction for it to be in a loop.
> 3. Try all possible obstacle positions!

This does work, but I feel there are still better solutions that I haven't found yet (on top of the improvements mentioned in Part A).

```python
import copy

guardPositions = set()


def solve(input):
    grid = []

    # Parses the grid
    for line in input:
        grid.append(list(line))

    guardx = 0
    guardy = 0

    # Finds the guard
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "^":
                guardx = x
                guardy = y

    # Gets all positions the guard walks
    runGuard(grid, guardx, guardy)

    # Places an obstacle in each tile the guard passes through and checks for a cycle
    validObjPos = []

    for pos in guardPositions:
        currTiles = set()
        newGrid = copy.deepcopy(grid)

        newGrid[pos[1]][pos[0]] = "#"
        if findCycle(newGrid, guardx, guardy, currTiles):
            validObjPos.append(pos)

    return len(validObjPos)


def findCycle(grid, guardx, guardy, tiles):
    facing = "up"
    # While the guard is in bounds
    while not (
        (guardx <= 0 and facing == "left")
        or (guardx >= len(grid[0]) - 1 and facing == "right")
        or (guardy <= 0 and facing == "up")
        or (guardy >= len(grid) - 1 and facing == "down")
    ):
        if facing == "up":
            guardy -= 1
            if grid[guardy][guardx] == "#":
                facing = "right"
                guardy += 1
                continue

        elif facing == "right":
            guardx += 1
            if grid[guardy][guardx] == "#":
                facing = "down"
                guardx -= 1
                continue

        elif facing == "down":
            guardy += 1
            if grid[guardy][guardx] == "#":
                facing = "left"
                guardy -= 1
                continue

        elif facing == "left":
            guardx -= 1
            if grid[guardy][guardx] == "#":
                facing = "up"
                guardx += 1
                continue

        # Detect cycle
        if (guardx, guardy, facing) in tiles:
            return True

        tiles.add((guardx, guardy, facing))

    return False


def runGuard(grid, guardx, guardy):
    facing = "up"
    # While the guard is in bounds
    while not (
        (guardx <= 0 and facing == "left")
        or (guardx >= len(grid[0]) - 1 and facing == "right")
        or (guardy <= 0 and facing == "up")
        or (guardy >= len(grid) - 1 and facing == "down")
    ):
        if facing == "up":
            guardy -= 1
            if grid[guardy][guardx] == "#":
                facing = "right"
                guardy += 1
                continue

        elif facing == "right":
            guardx += 1
            if grid[guardy][guardx] == "#":
                facing = "down"
                guardx -= 1
                continue

        elif facing == "down":
            guardy += 1
            if grid[guardy][guardx] == "#":
                facing = "left"
                guardy -= 1
                continue

        elif facing == "left":
            guardx -= 1
            if grid[guardy][guardx] == "#":
                facing = "up"
                guardx += 1
                continue

        guardPositions.add((guardx, guardy))

```
