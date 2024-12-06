def solve(input):

    totalDistance = 0

    left = []
    right = []

    for line in input:
        left.append(line.split("   ")[0])
        right.append(line.split("   ")[1])

    left = sorted(left)
    right = sorted(right)

    for i in range(len(left)):
        totalDistance += abs(int(left[i]) - int(right[i]))

    return totalDistance
