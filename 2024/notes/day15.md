# [Day 15 - Warehouse Woes](https://adventofcode.com/2024/day/15)

> [<- Previous](day14.md) | [Next ->](day16.md)

Maybe it's from finals week, or not getting enough sleep, or something else, but this took me **wayyyyy** longer than it should have. I did take a break during Part B,
but I had so many edge cases that I didn't of and my code is definitely a mess, might have to do some refactoring later.

Really cool problem though, and it was something I mentioned back in [Day 6](day06.md)!

|                | Part A | Part B  |  Total  |
| -------------- | :----: | :-----: | :-----: |
| Coding Time    | 33:48  | 2:20:04 | 2:53:52 |
| Execution Time | 0.003s | 0.007s  | 0.011s  |

## Part A

This also can be broken down into 3 stages.

1. For parsing, you have to store the "map" of the board and also parse out the instructions
2. Run the instructions on the robot and move everything accordingly
3. Calculate the "gps position" of all the boxes to get the resulting submission

> [!TIP]
> A nice thing to do is to make the "pushing" of the boxes recursive, so every box will push on the other boxes in front of it. If one of them encounters a wall, then the
> whole chain returns `False` and terminates, leaving everthing the way it was.

```python
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

```

## Part B

Ahhh Part B, my arch nemesis. Looking back, I definitely should have refactored my code a lot sooner than I did.

After getting the double-wide parsing setup, I thought it would be easy to just modify the up and down box pushes and submit. Boy was I wrong.

My main issue was the recursive way I was pushing the boxes. It could handle the 2-wide boxes no problem, but the issue came when one of the boxes wolud get stuck
and the other was free to move.

- The robot is pushing up on the center box
- The right box is currently blocked by the wall above, so it shouldn't move
- The left box is free to move, so it will do so (_which is incorrect behavior_)

Before:

```
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############
```

After:

```
##############
##...[].##..##
##.....[]...##
##....[]....##
##.....@....##
##..........##
##############
```

> I was trying to turn this into a small gif animation, if only I can recreate my issue!

I had to split up my recursive "pushBox" into a "move check" (called `checkBox` in the code) and a "push box" (still called `pushBox`). That way it can check if
ALL boxes can move before physically moving them.

The really annoying part is that this case is never encountered through the test cases, so I had to iterate through each move and watch what the bot was doing. Pretty cool to
see sped up though.

I also had other issues, such as boxes overlapping or spawning out of thin air (before I checked if `pushBox` was actually acting on a box).

> [!TIP]
> Don't hold onto your Part A code!!!! It might not work exactly the right fit for Part B and can cost you a lot of time and headaches in the long run.

Also cool gif I made, with the help of [terminalizer](https://github.com/faressoft/terminalizer):

<p align="center">
    <img src ="../code/Day15/game.gif" alt="Part B running in the terminal">
</p>

```python
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
        # print(i)
        # display(grid, robotx, roboty)
        # input("enter")
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

```

