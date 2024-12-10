# [Day 4 - Ceres Search](https://adventofcode.com/2024/day/4)

> [<- Previous](day03.md) | [Next ->](day05.md)

It's word search time. I'm sure this could have went smoother if I had more helper functions but alas.

Pretty much hard-coded everything, definitely could be improved to be more modular.

|                | Part A | Part B | Total  |
| -------------- | :----: | :----: | :----: |
| Coding Time\*  |        |  7:26  |        |
| Execution Time | 0.006s | 0.002s | 0.008s |

> \*Time is not recorded as this day was started later rather than at midnight, so no accurate time for part 1 can be recorded

## Part A

Pretty self explanatory, just going through each case and matching it against a hard-coded string. As mentioned above, this definitely can be improved to be more concise
and modular.

```python
def solve(input):
    total = 0
    matrix = []

    for line in input:
        matrix.append(list(line))

    # Horizontal
    for y in range(len(matrix)):
        for x in range(len(matrix[0]) - 3):
            if (
                matrix[y][x] == "X"
                and matrix[y][x + 1] == "M"
                and matrix[y][x + 2] == "A"
                and matrix[y][x + 3] == "S"
            ):
                total += 1
            if (
                matrix[y][x] == "S"
                and matrix[y][x + 1] == "A"
                and matrix[y][x + 2] == "M"
                and matrix[y][x + 3] == "X"
            ):
                total += 1

    # Vertical
    for y in range(len(matrix) - 3):
        for x in range(len(matrix[0])):
            if (
                matrix[y][x] == "X"
                and matrix[y + 1][x] == "M"
                and matrix[y + 2][x] == "A"
                and matrix[y + 3][x] == "S"
            ):
                total += 1
            if (
                matrix[y][x] == "S"
                and matrix[y + 1][x] == "A"
                and matrix[y + 2][x] == "M"
                and matrix[y + 3][x] == "X"
            ):
                total += 1

    # Positive Diagonal
    for y in range(len(matrix) - 3):
        for x in range(len(matrix[0]) - 3):
            if (
                matrix[y][x] == "X"
                and matrix[y + 1][x + 1] == "M"
                and matrix[y + 2][x + 2] == "A"
                and matrix[y + 3][x + 3] == "S"
            ):
                total += 1
            if (
                matrix[y][x] == "S"
                and matrix[y + 1][x + 1] == "A"
                and matrix[y + 2][x + 2] == "M"
                and matrix[y + 3][x + 3] == "X"
            ):
                total += 1

    # Negative Diagonal
    for y in range(3, len(matrix)):
        for x in range(len(matrix[0]) - 3):
            if (
                matrix[y][x] == "X"
                and matrix[y - 1][x + 1] == "M"
                and matrix[y - 2][x + 2] == "A"
                and matrix[y - 3][x + 3] == "S"
            ):
                total += 1
            if (
                matrix[y][x] == "S"
                and matrix[y - 1][x + 1] == "A"
                and matrix[y - 2][x + 2] == "M"
                and matrix[y - 3][x + 3] == "X"
            ):
                total += 1

    return total

```

## Part B

Honestly much easier than Part A. I used a similar concept, but matched the center of the 'X' and all 4 possible states the 'MAS' can be in.

```python
def solve(input):
    total = 0
    matrix = []

    for line in input:
        matrix.append(list(line))

    # Find an A
    for y in range(1, len(matrix) - 1):
        for x in range(1, len(matrix[0]) - 1):
            if matrix[y][x] != "A":
                continue

            # Check for the crosses
            if (
                matrix[y - 1][x - 1] == "M"
                and matrix[y + 1][x + 1] == "S"
                and matrix[y + 1][x - 1] == "M"
                and matrix[y - 1][x + 1] == "S"
            ):
                total += 1
            elif (
                matrix[y - 1][x - 1] == "S"
                and matrix[y + 1][x + 1] == "M"
                and matrix[y + 1][x - 1] == "M"
                and matrix[y - 1][x + 1] == "S"
            ):
                total += 1
            elif (
                matrix[y - 1][x - 1] == "M"
                and matrix[y + 1][x + 1] == "S"
                and matrix[y + 1][x - 1] == "S"
                and matrix[y - 1][x + 1] == "M"
            ):
                total += 1
            elif (
                matrix[y - 1][x - 1] == "S"
                and matrix[y + 1][x + 1] == "M"
                and matrix[y + 1][x - 1] == "S"
                and matrix[y - 1][x + 1] == "M"
            ):
                total += 1

    return total

```
