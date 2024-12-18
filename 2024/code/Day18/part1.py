from queue import PriorityQueue


def solve(input):
    size = 71
    fallen = 1024

    blockers = []

    for line in input:
        # Only calculate the amount needed
        if fallen <= 0:
            break
        x, y = list(map(int, line.split(",")))
        blockers.append((x, y))
        fallen -= 1

    minSteps = 0

    visited = set()
    queue = PriorityQueue()
    queue.put((0, (0, 0)))

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while not queue.empty():
        steps, (x, y) = queue.get()

        # Skip if we already saw this node
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Found the exit
        if x == size - 1 and y == size - 1:
            minSteps = steps
            break

        # Add neighbors
        for dx, dy in dirs:
            if (x + dx) < 0 or (x + dx) >= size or (y + dy) < 0 or (y + dy) >= size:
                continue

            if (x + dx, y + dy) not in blockers:
                queue.put((steps + 1, (x + dx, y + dy)))

    return minSteps
