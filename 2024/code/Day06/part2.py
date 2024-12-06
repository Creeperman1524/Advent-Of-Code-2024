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
