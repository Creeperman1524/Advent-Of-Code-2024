from queue import PriorityQueue


def solve(input):
    maze = []

    for line in input:
        maze.append(list(line))

    s = (0, 0)
    e = (0, 0)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "S":
                s = (x, y)
            if maze[y][x] == "E":
                e = (x, y)

    visited = set()
    # Contains the lowest cost found from the starting node to that node
    costs = {}
    # costs[(s[0], s[1])] = 0

    # A queue of neighbors to search next
    queue = PriorityQueue()
    queue.put((0, s))

    # Performs Dijkstra's Algorithm to get the costs to each node
    dirs = {(1, 0), (-1, 0), (0, 1), (0, -1)}
    while not queue.empty():
        cost, (x, y) = queue.get()
        key = (x, y)

        # Skip if we already saw this node
        if key in visited:
            continue
        visited.add(key)

        # Found the exit
        if maze[y][x] == "E":
            costs[key] = cost + 1
            break

        for dx, dy in dirs:
            # Bounds checking
            if (
                x + dx < 0
                or x + dx > len(maze[y])
                or y + dy < 0
                or y + dy > len(maze)
                or maze[y + dy][x + dx] == "#"
                or (x + dx, y + dy) in visited
            ):
                continue

            queue.put((cost + 1, (x + dx, y + dy)))

            # Every node we hit will always be the min
            costs[key] = cost + 1

    # Find the max cost savings
    bigSavings = 0
    savingsArr = []

    for node in costs.keys():
        for otherNode in costs.keys():
            if node == otherNode:
                continue

            manhattanDistance = abs(node[0] - otherNode[0]) + abs(
                node[1] - otherNode[1]
            )
            if manhattanDistance > 20:
                continue

            savings = costs[otherNode] - costs[node] - manhattanDistance
            savingsArr.append(savings)

            if savings >= 100:
                bigSavings += 1

    return bigSavings
