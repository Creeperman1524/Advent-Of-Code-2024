def solve(input):
    grid = []

    for line in input:
        grid.append(list(line))

    visited = set()

    islands = []

    # Create a DFS Forest
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) not in visited:
                islands.append(dfs(grid, x, y, visited))

    # Calculates the area and perimeter
    totalPrice = 0
    for plantIsland in islands:
        area = len(plantIsland)

        perimeter = 0
        calculated = set()
        for plant in plantIsland:

            neighbors = 0
            x = plant[0]
            y = plant[1]

            if y > 0 and (x, y - 1) in calculated:
                neighbors += 1

            # Down
            if y < len(grid) - 1 and (x, y + 1) in calculated:
                neighbors += 1

            # Left
            if x > 0 and (x - 1, y) in calculated:
                neighbors += 1

            # Right
            if x < len(grid[0]) - 1 and (x + 1, y) in calculated:
                neighbors += 1

            # 0 neighbors = 4 perimeter
            # 1 neighbors = 2 perimeter
            # 2 neighbors = 0 perimeter
            # 3 neighbors = -2 perimeter
            # 4 neighbors = -4 perimeter
            perimeter += -2 * (neighbors - 2)

            calculated.add(plant)

        totalPrice += area * perimeter

    return totalPrice


# Runs a dfs on a specific plant type
def dfs(grid, x, y, visited):
    if (x, y) in visited:
        return

    island = []
    visited.add((x, y))

    plant = grid[y][x]

    # Up
    if y > 0 and grid[y - 1][x] == plant:
        up = dfs(grid, x, y - 1, visited)
        if up != None:
            island.extend(up)

    # Down
    if y < len(grid) - 1 and grid[y + 1][x] == plant:
        down = dfs(grid, x, y + 1, visited)
        if down != None:
            island.extend(down)

    # Left
    if x > 0 and grid[y][x - 1] == plant:
        left = dfs(grid, x - 1, y, visited)
        if left != None:
            island.extend(left)

    # Right
    if x < len(grid[0]) - 1 and grid[y][x + 1] == plant:
        right = dfs(grid, x + 1, y, visited)
        if right != None:
            island.extend(right)

    island.append((x, y))

    return island
