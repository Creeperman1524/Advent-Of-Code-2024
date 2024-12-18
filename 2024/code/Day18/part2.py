from queue import PriorityQueue


def solve(input):
    size = 71

    blockers = []
    bestPath = []
    counter = 0

    for line in input:
        counter += 1
        bx, by = list(map(int, line.split(",")))
        blockers.append((bx, by))

        # Part A guarantees bytes up to 1024 have a safe path
        if counter < 1024:
            continue

        # Skip simulating new paths for blockers that do not fall on the current path
        if (bx, by) not in bestPath and len(bestPath) > 0:
            continue

        # Calculate the best path given the blockers
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
                newX, newY = x + dx, y + dy
                if (
                    not (0 < newX < size)
                    or not (0 < newY < size)
                    or (newX, newY) in blockers
                    or (newX, newY) in visited
                ):
                    continue

                queue.put((steps + 1, (newX, newY)))
                pathDict[(newX, newY)] = (x, y)

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
