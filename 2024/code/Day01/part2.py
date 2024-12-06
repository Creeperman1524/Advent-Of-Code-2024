from collections import Counter


def solve(input):

    similarity = 0

    left = []
    right = []

    for line in input:
        left.append(line.split("   ")[0])
        right.append(line.split("   ")[1])

    c = Counter(right)

    for i in range(len(left)):
        similarity += int(left[i]) * c[left[i]]

    return similarity
