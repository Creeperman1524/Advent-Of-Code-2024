from queue import PriorityQueue


def solve(input):
    size = 71

    blockers = []
    bestPath = []

    for line in input:
        bx, by = list(map(int, line.split(",")))
        blockers.append((bx, by))

        # Skip simulating new paths for blockers that do not fall on the current path
        if (bx, by) not in bestPath and len(bestPath) > 0:
            continue

        visited = set()
        queue = PriorityQueue()
        queue.put((0, (0, 0)))
        pathDict = {}

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        escaped = False
        while not queue.empty():
            steps, (x, y) = queue.get()

            # Skip if we already saw this node
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Found the exit
            if x == size - 1 and y == size - 1:
                escaped = True
                break

            # Add neighbors
            for dx, dy in dirs:
                if (x + dx) < 0 or (x + dx) >= size or (y + dy) < 0 or (y + dy) >= size:
                    continue

                if (x + dx, y + dy) not in blockers and (x + dx, y + dy) not in visited:
                    queue.put((steps + 1, (x + dx, y + dy)))
                    pathDict[(x + dx, y + dy)] = (x, y)

        if escaped:
            # Save the new path after a blocker appeared on it
            bestPath.clear()
            node = (size - 1, size - 1)
            while node != (0, 0):
                bestPath.append(node)
                node = pathDict[node]

            bestPath.append

        else:
            # Return the blocker that first stopped our path
            return (bx, by)

    return "Always possible"
