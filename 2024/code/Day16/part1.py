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

    minCost = -1

    visited = set()
    queue = PriorityQueue()
    queue.put((0, s, 1))

    dirs = {1: (1, 0), 3: (-1, 0), 2: (0, 1), 0: (0, -1)}
    while not queue.empty():
        cost, (x, y), dir = queue.get()

        # Skip if we already saw this node
        if (x, y, dir) in visited:
            continue
        visited.add((x, y, dir))

        # Found the exit
        if maze[y][x] == "E":
            minCost = cost
            break

        # Continue straight
        dx, dy = dirs[dir]
        neighbor = maze[y + dy][x + dx]

        if neighbor != "#":
            queue.put((cost + 1, (x + dx, y + dy), dir))

        # Turn to other direcctions
        queue.put((cost + 1000, (x, y), (dir - 1) % 4))
        queue.put((cost + 1000, (x, y), (dir + 1) % 4))

    return minCost
