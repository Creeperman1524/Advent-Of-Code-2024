def solve(input):
    grid = []
    instructions = ""

    # Parses the grid
    parseDirs = False
    for line in input:
        if len(line) == 0:
            parseDirs = True
            continue

        if not parseDirs:
            grid.append(list(line))
        else:
            instructions += line

    # Find the robot
    robotx = 0
    roboty = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "@":
                robotx = x
                roboty = y

    # Run the instructions
    for i in instructions:
        if i == "^":
            # Border
            if grid[roboty - 1][robotx] == "#":
                continue

            # Boxes
            if grid[roboty - 1][robotx] == "O":
                if not pushBox(grid, robotx, roboty - 1, i):
                    continue

            roboty -= 1

        elif i == ">":
            # Border
            if grid[roboty][robotx + 1] == "#":
                continue

            # Boxes
            if grid[roboty][robotx + 1] == "O":
                if not pushBox(grid, robotx + 1, roboty, i):
                    continue

            robotx += 1

        elif i == "v":
            # Border
            if grid[roboty + 1][robotx] == "#":
                continue

            # Boxes
            if grid[roboty + 1][robotx] == "O":
                if not pushBox(grid, robotx, roboty + 1, i):
                    continue

            roboty += 1

        elif i == "<":
            # Border
            if grid[roboty][robotx - 1] == "#":
                continue

            # Boxes
            if grid[roboty][robotx - 1] == "O":
                if not pushBox(grid, robotx - 1, roboty, i):
                    continue

            robotx -= 1

    # Calculate the box coordinates
    gpsCoordinates = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "O":
                gpsCoordinates += 100 * y + x

    return gpsCoordinates


def pushBox(grid, x, y, dir):
    if dir == "^":
        # Border
        if grid[y - 1][x] == "#":
            return False

        # Cascade boxes
        if grid[y - 1][x] == "O":
            if not pushBox(grid, x, y - 1, dir):
                return False

        # Moves the box
        grid[y - 1][x] = "O"
        grid[y][x] = "."
        return True

    elif dir == ">":
        # Border
        if grid[y][x + 1] == "#":
            return False

        # Cascade boxes
        if grid[y][x + 1] == "O":
            if not pushBox(grid, x + 1, y, dir):
                return False

        # Moves the box
        grid[y][x + 1] = "O"
        grid[y][x] = "."
        return True

    elif dir == "v":
        # Border
        if grid[y + 1][x] == "#":
            return False

        # Cascade boxes
        if grid[y + 1][x] == "O":
            if not pushBox(grid, x, y + 1, dir):
                return False

        # Moves the box
        grid[y + 1][x] = "O"
        grid[y][x] = "."
        return True

    elif dir == "<":
        # Border
        if grid[y][x - 1] == "#":
            return False

        # Cascade boxes
        if grid[y][x - 1] == "O":
            if not pushBox(grid, x - 1, y, dir):
                return False

        # Moves the box
        grid[y][x - 1] = "O"
        grid[y][x] = "."
        return True


def display(grid, robotx, roboty):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if x == robotx and y == roboty:
                print("@", end="")
            elif grid[y][x] == "O":
                print("O", end="")
            elif grid[y][x] == "#":
                print("#", end="")
            else:
                print(".", end="")

        print("")

    print("")
