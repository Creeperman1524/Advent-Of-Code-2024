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
