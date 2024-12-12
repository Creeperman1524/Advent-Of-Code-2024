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

    # Calculates the area and side count
    totalPrice = 0
    for plantIsland in islands:
        area = len(plantIsland)

        # Calculates all edges of the squares, removing duplicate edges (as they would be inside the region)

        # A list of coordinate pairs of the edges of each region ((x1, y1), (x2, y2))
        edges = list()
        for plant in plantIsland:
            x = plant[0]
            y = plant[1]

            # Adds all the edges of the square (with it's coordinate being top left)
            newEdges = [
                ((x, y), (x, y + 1)),
                ((x, y), (x + 1, y)),
                ((x, y + 1), (x + 1, y + 1)),
                ((x + 1, y), (x + 1, y + 1)),
            ]

            # Remove duplicates
            for new in newEdges:
                if new in edges:
                    edges.remove(new)
                else:
                    edges.append(new)

        # # of horizontal lines = # of vertical lines
        # Just find number of horizontal lines * 2 = sides

        # Adds a horizontal line, continually connects it to other edge until it can't find anymore
        # Increment the side count, add a new edge to search for that side and repeat until there are no more edges to add
        sides = 0
        usedEdges = []
        for edge1 in edges:
            # The edge we're trying to connect to, skipping used/veritcal
            if edge1 in usedEdges or edge1[0][0] == edge1[1][0]:
                continue
            sides += 1
            usedEdges.append(edge1)

            changed = True
            while changed:
                changed = False
                for edge2 in edges:
                    # The edge we're checking to see if it connects to it, skipping used/vertical
                    if edge2 in usedEdges or edge2[0][0] == edge2[1][0]:
                        continue

                    # Edges do not connect if there is a vertical line in between them
                    if edge1[0] == edge2[1]:
                        if (edge1[0], (edge1[0][0], edge1[0][1] + 1)) in edges or (
                            edge1[0],
                            (edge1[0][0], edge1[0][1] - 1),
                        ) in edges:
                            continue
                    elif edge1[1] == edge2[0]:
                        if (edge2[0], (edge2[0][0], edge2[0][1] + 1)) in edges or (
                            edge2[0],
                            (edge2[0][0], edge2[0][1] - 1),
                        ) in edges:
                            continue

                    # Lines connect if they share 1 coordinate
                    if edge1[0] == edge2[1]:
                        changed = True
                        usedEdges.append(edge2)

                        # Extends the edge to search for more candidates
                        edge1 = (edge2[0], edge1[1])
                    elif edge1[1] == edge2[0]:
                        changed = True
                        usedEdges.append(edge2)

                        # Extends the edge to search for more candidates
                        edge1 = (edge1[0], edge2[1])

        totalPrice += area * sides * 2

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
