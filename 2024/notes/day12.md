# [Day 12 - Garden Groups](https://adventofcode.com/2024/day/12)

> [<- Previous](day11.md) | [Next ->](day13.md)

More grid/graph problems! Yippee!! Although this one was a tough one (for me), especially with Part B. I am learning I definitely should brush up on my
graph skills for future reference.

**Beware of the yap session below!**

|                | Part A | Part B  |  Total  |
| -------------- | :----: | :-----: | :-----: |
| Coding Time    | 33:52  | 1:29:21 | 2:03:13 |
| Execution Time | 0.04s  | 0.242s  | 0.282s  |

## Part A

This one was a two step process. First, I needed to separate out the groups of different plants. I immediately recognized this as creating a DFS/BFS forest
(Get it? Because instead of a tree, it's multiple trees!)

I essentially ran a [DFS](https://en.wikipedia.org/wiki/Depth-first_search) algorithm for each _unvisited_ part of the grid, linking together all the different plots
of flowers. This gave me an array of arrays of coordinates for each tile in each plot of a specific flower group.

Then, I could find the area simply by taking the length of the array containing each coordinates of the flowers (as the area is just the number of flowers!). However,
the perimeter of the plots proved to be a little more challenging...

> [!TIP]
> While thinking this problem through, I realized I could iteratively find out the perimeter one tile at a time. The rules are as follows:
>
> 1. If a added tile has 0 current neighbors, then it has a perimeter of 4
> 2. 1 neighbor, perimeter = 3 lines that it adds - 1 that it blocks = 2
> 3. 2 neighbors, perimeter = 2 lines that it adds - 2 that it blocks = 0
> 4. 3 neighbors, perimeter = 1 line that it adds - 3 that it blocks = -2
> 5. 4 neighbors, perimeter = 0 lines that it adds - 4 that it blocks = -4
>
> That way, I can loop over each tile from the DFS forest and calculate the perimeter (and thus price of fencing) for each plot!
>
> This could also potentially be added to the DFS itself while it is finding new plants to add, so a potential optimization there.

```python
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

```

## Part B

As you can tell from the time spent on Part A and Part B, I really struggled with Part B. The issue was that instead of counting the perimeter of the plots, we
needed to count the _sides_ of the plots.

First I decided it would be wise to find every edge of the plot. This is essentially a much harder version of Part A, but after some notebook drawings I figure it out easily.
Then came the issue of _merging_ together these edges to be able to count the sides of each plot, which was a lot more difficult than I thought.

> [!TIP]
> My first insight to the problem was that the number of veritcal sides/edges and horizontal sides/edges were always equal. The proof of this? No idea, but from my
> rough diagrams and looking at the examples, I decided to go with this fact.
>
> This way, I only had to worry about counting the number of horizontal sides and could multiply the amount `* 2` in the end

> [!TIP]
> My second idea was to try a greedy approach to merging together the edges. I would search the candidate edges for a valid match (no vertical line separating them,
> both were horizontal lines, and had matching endpoints), and then extend the current side I was looking at. After finding no valid matches, I would move onto
> another edge to start working on another side.
>
> I added in the "no vertical line separating" last as it messed with the last test case of essentially creating merged fencing in areas it should not be

To my surprise, after implementing this and checking it against the test cases (and fixing the error above), it worked! And pretty quickly too.

I'm sure there is a _much_ better algorithm than this, but it runs just find and I understand how it works! I count that as a win.

```python
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

```

