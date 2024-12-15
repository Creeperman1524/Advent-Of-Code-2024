def solve(inputStuff):
    grid = []
    instructions = ""

    # Parses the grid
    parseDirs = False
    for line in inputStuff:
        if len(line) == 0:
            parseDirs = True
            continue

        if not parseDirs:
            row = []
            for x in line:
                if x == "#":
                    row.extend(["#", "#"])
                elif x == "O":
                    row.extend(["[", "]"])
                elif x == ".":
                    row.extend([".", "."])
                elif x == "@":
                    row.extend(["@", "."])

            grid.append(row)
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
                grid[y][x] = "."

    # display(grid, robotx, roboty)

    # Run the instructions
    for i in instructions:
        print(i)
        display(grid, robotx, roboty)
        input("enter")
        if i == "^":
            # Border
            if grid[roboty - 1][robotx] == "#":
                continue

            # Boxes
            if grid[roboty - 1][robotx] == "[" or grid[roboty - 1][robotx] == "]":
                if not checkBox(grid, robotx, roboty - 1, i):
                    continue
                pushBox(grid, robotx, roboty - 1, i)

            roboty -= 1

        elif i == ">":
            # Border
            if grid[roboty][robotx + 1] == "#":
                continue

            # Boxes
            if grid[roboty][robotx + 1] == "[" or grid[roboty][robotx + 1] == "]":
                if not checkBox(grid, robotx + 1, roboty, i):
                    continue
                pushBox(grid, robotx + 1, roboty, i)

            robotx += 1

        elif i == "v":
            # Border
            if grid[roboty + 1][robotx] == "#":
                continue

            # Boxes
            if grid[roboty + 1][robotx] == "[" or grid[roboty + 1][robotx] == "]":
                if not checkBox(grid, robotx, roboty + 1, i):
                    continue
                pushBox(grid, robotx, roboty + 1, i)

            roboty += 1

        elif i == "<":
            # Border
            if grid[roboty][robotx - 1] == "#":
                continue

            # Boxes
            if grid[roboty][robotx - 1] == "[" or grid[roboty][robotx - 1] == "]":
                if not checkBox(grid, robotx - 1, roboty, i):
                    continue
                pushBox(grid, robotx - 1, roboty, i)

            robotx -= 1

    # display(grid, robotx, roboty)

    # Calculate the box coordinates
    gpsCoordinates = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "[":
                gpsCoordinates += 100 * y + x

    return gpsCoordinates


def pushBox(grid, x, y, dir):
    if grid[y][x] not in ["[", "]"]:
        return

    # Normalize to the coordinates of the left side of the box
    if grid[y][x] == "]":
        x -= 1

    if dir == "^":
        # Cascade boxes
        pushBox(grid, x, y - 1, dir)
        pushBox(grid, x + 1, y - 1, dir)

        # Moves the box
        grid[y - 1][x] = "["
        grid[y - 1][x + 1] = "]"
        grid[y][x] = "."
        grid[y][x + 1] = "."

    elif dir == ">":
        # Cascade boxes
        pushBox(grid, x + 2, y, dir)

        # Moves the box
        grid[y][x] = "."
        grid[y][x + 1] = "["
        grid[y][x + 2] = "]"

    elif dir == "v":
        pushBox(grid, x, y + 1, dir)
        pushBox(grid, x + 1, y + 1, dir)

        # Moves the box
        grid[y + 1][x] = "["
        grid[y + 1][x + 1] = "]"
        grid[y][x] = "."
        grid[y][x + 1] = "."

    elif dir == "<":
        pushBox(grid, x - 1, y, dir)

        # Moves the box
        grid[y][x - 1] = "["
        grid[y][x] = "]"
        grid[y][x + 1] = "."


# Checks if a box can move, checking recursively downstream of it
def checkBox(grid, x, y, dir):
    if grid[y][x] not in ["[", "]"]:
        return True

    # Normalize to the coordinates of the left side of the box
    if grid[y][x] == "]":
        x -= 1

    if dir == "^":
        # Border
        if grid[y - 1][x] == "#" or grid[y - 1][x + 1] == "#":
            return False

        # Checks if the other boxes can move
        if not checkBox(grid, x, y - 1, dir) or not checkBox(grid, x + 1, y - 1, dir):
            return False

    elif dir == ">":
        # Border
        if grid[y][x + 2] == "#":
            return False

        if not checkBox(grid, x + 2, y, dir):
            return False

    elif dir == "v":
        # Border
        if grid[y + 1][x] == "#" or grid[y + 1][x + 1] == "#":
            return False

        if not checkBox(grid, x, y + 1, dir) or not checkBox(grid, x + 1, y + 1, dir):
            return False

    elif dir == "<":
        # Border
        if grid[y][x - 1] == "#":
            return False

        if not checkBox(grid, x - 1, y, dir):
            return False

    return True


def display(grid, robotx, roboty):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if x == robotx and y == roboty:
                print("@", end="")
            elif grid[y][x] != "@":
                print(grid[y][x], end="")

        print("")

    print("")
