# [Day 8 - Resonant Collinearity](https://adventofcode.com/2024/day/8)

> [<- Previous](day07.md) | [Next ->](day09.md)

General comments about the problem

Honestly a pretty easy day compared to the rest so far. Took a little work with the data structures
but the solution essentialy wrote itself.

|                | Part A | Part B | Total |
| -------------- | :----: | :----: | :---: |
| Coding Time\*  |        | 15:40  |       |
| Execution Time |  < 0s  |  < 0s  | < 0s  |

> \*Time is not recorded as this day was started later rather than at midnight, so no accurate time for part 1 can be recorded

## Part A

I think a reasonable way to do this would be to loop over every position in the grid to determine if they are in "resonance" with any of the frequencies.
However, I decided to go the opposite way of finding the anitnodes of each frequency, which definitely improved the runtime of the program.

```python
def solve(input):
    total = 0
    matrix = []

    for line in input:
        matrix.append(list(line))

    antinodes = set()
    freqs = dict()

    # Finds all frequencies and their positions
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            elem = matrix[y][x]
            if elem == ".":
                continue

            if elem in freqs:
                freqs[elem].append((x, y))
            else:
                freqs[elem] = [(x, y)]

    # Goes through each pairs of positions for each frequency
    for freq in freqs.values():
        for pos1 in freq:
            for pos2 in freq:
                if pos1 == pos2:
                    continue

                diffx = -2 * (pos1[0] - pos2[0])
                diffy = -2 * (pos1[1] - pos2[1])

                newx = pos1[0] + diffx
                newy = pos1[1] + diffy

                # Ignore out of bounds antinodes
                if (
                    newx < 0
                    or newy < 0
                    or newx >= len(matrix[0])
                    or newy >= len(matrix)
                ):
                    continue

                antinodes.add((newx, newy))

    return len(antinodes)

```

## Part B

Almost exactly the same as Part A, but just repeatedly adding the "vector" of the towers to each point until they go outside the bounds of the grid.

(And also sneakily adding in the antinodes that rest on each of the towers as my program didn't handle the different signs of the vector too well)

```python
def solve(input):
    matrix = []

    for line in input:
        matrix.append(list(line))

    antinodes = set()
    freqs = dict()

    # Finds all frequencies and their positions
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            elem = matrix[y][x]
            if elem == ".":
                continue

            if elem in freqs:
                freqs[elem].append((x, y))
            else:
                freqs[elem] = [(x, y)]

    # Goes through each pairs of positions for each frequency
    for freq in freqs.values():
        for pos1 in freq:
            for pos2 in freq:
                if pos1 == pos2:
                    continue

                newx = 0
                newy = 0
                mult = 2

                # Keep adding antinodes until it's out of bounds
                while (
                    newx >= 0
                    and newy >= 0
                    and newx < len(matrix[0])
                    and newy < len(matrix)
                ):
                    diffx = -1 * mult * (pos1[0] - pos2[0])
                    diffy = -1 * mult * (pos1[1] - pos2[1])

                    newx = pos1[0] + diffx
                    newy = pos1[1] + diffy

                    if (
                        newx < 0
                        or newy < 0
                        or newx >= len(matrix[0])
                        or newy >= len(matrix)
                    ):
                        continue

                    antinodes.add((newx, newy))

                    mult += 1

            # Add the nodes that appear on every antenna
            antinodes.add((pos1[0], pos1[1]))

    return len(antinodes)

```
