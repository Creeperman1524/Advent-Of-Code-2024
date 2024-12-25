def solve(input):
    towels = []
    designs = []

    count = 0
    for line in input:
        if count == 0:
            towels = line.strip().split(", ")
        elif count == 1:
            pass
        else:
            designs.append(line.strip())

        count += 1

    ways = 0
    counter = 0

    reachable = {}
    for design in designs:
        counter += 1
        # print(counter, design)
        ways += checkDesign(design, towels, reachable)

    return ways


def checkDesign(design, towels, reachable):
    if len(design) == 0:
        return 1

    if design in reachable:
        return reachable[design]

    ways = 0
    for towel in towels:
        towelLen = len(towel)

        if towelLen <= len(design) and design[:towelLen] == towel:
            ways += checkDesign(design[towelLen:], towels, reachable)

    reachable[design] = ways

    return ways
