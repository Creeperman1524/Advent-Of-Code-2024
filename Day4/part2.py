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
