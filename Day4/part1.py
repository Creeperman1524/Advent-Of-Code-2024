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
