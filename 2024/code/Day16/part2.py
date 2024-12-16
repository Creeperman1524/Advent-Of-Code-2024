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
    costs[(s[0], s[1], 1)] = 0

    # Contains the best path(s) from that node back to the start node
    fromNodes = {}

    # A queue of neighbors to search next
    queue = PriorityQueue()
    queue.put((0, s, 1))

    # This can probably be simplified by prefilling all the dictionaries
    # so no checks are needed
    def calculateNodes(keyToAdd, key, cost, costModifier):
        if keyToAdd in costs:
            if costs[keyToAdd] > cost + costModifier:
                # Found better path for keyToAdd, update it's score
                costs[keyToAdd] = cost + costModifier

                # Remove all previous paths
                fromNodes[keyToAdd] = set()
                fromNodes[keyToAdd].add(key)
            if costs[keyToAdd] == cost + costModifier:
                # Adds the backwards node
                if keyToAdd in fromNodes:
                    fromNodes[keyToAdd].add(key)
                else:
                    fromNodes[keyToAdd] = set()
                    fromNodes[keyToAdd].add(key)

        else:
            costs[keyToAdd] = costs[key] + costModifier
            # Adds the backwards node
            if keyToAdd in fromNodes:
                fromNodes[keyToAdd].add(key)
            else:
                fromNodes[keyToAdd] = set()
                fromNodes[keyToAdd].add(key)

    # Performs Dijkstra's Algorithm to get the costs to each node
    dirs = {1: (1, 0), 3: (-1, 0), 2: (0, 1), 0: (0, -1)}
    while not queue.empty():
        cost, (x, y), dir = queue.get()
        key = (x, y, dir)

        # Skip if we already saw this node
        if key in visited:
            continue
        visited.add(key)

        # Found the exit
        if maze[y][x] == "E":
            break

        # Continue straight
        dx, dy = dirs[dir]
        neighbor = maze[y + dy][x + dx]

        if neighbor != "#":
            straightKey = (x + dx, y + dy, dir)
            queue.put((cost + 1, (x + dx, y + dy), dir))
            calculateNodes(straightKey, key, cost, 1)

        # Turn to other direcctions
        queue.put((cost + 1000, (x, y), (dir - 1) % 4))
        leftKey = (x, y, (dir - 1) % 4)
        calculateNodes(leftKey, key, cost, 1000)

        queue.put((cost + 1000, (x, y), (dir + 1) % 4))
        rightKey = (x, y, (dir + 1) % 4)
        calculateNodes(rightKey, key, cost, 1000)

    # costs[(e[0], e[1], 0)] contains the answer for Part A

    # Traverses the fromNodes backwards to find all best paths
    goodSeats = set()

    def dfs(fromNodes, currNode, s):
        for neighbor in fromNodes[currNode]:
            x, y, _ = neighbor

            goodSeats.add((x, y))
            if (x, y) == s:
                return

            dfs(fromNodes, neighbor, s)

        return

    goodSeats.add(e)
    dfs(fromNodes, (e[0], e[1], 0), s)

    return len(goodSeats)
