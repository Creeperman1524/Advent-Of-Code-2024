def solve(input):
    scores = 0

    grid = []

    # Parses the grid
    for line in input:
        grid.append(list(map(int, line)))

    # Run a search on all 0s
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:

                score = search(grid, x, y)
                scores += score

    return scores


# A search from a 0 to all reachable 9s
def search(grid, x, y):
    elem = grid[y][x]
    if elem == 9:
        return 1

    score = 0

    # Up
    if y > 0 and grid[y - 1][x] == elem + 1:
        score += search(grid, x, y - 1)

    # Down
    if y < len(grid) - 1 and grid[y + 1][x] == elem + 1:
        score += search(grid, x, y + 1)

    # Left
    if x > 0 and grid[y][x - 1] == elem + 1:
        score += search(grid, x - 1, y)

    # Right
    if x < len(grid[0]) - 1 and grid[y][x + 1] == elem + 1:
        score += search(grid, x + 1, y)

    return score
