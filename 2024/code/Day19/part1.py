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

    possible = 0
    counter = 0

    unreachable = set()
    for design in designs:
        counter += 1
        # print(counter, design)
        if checkDesign(design, towels, unreachable):
            possible += 1

    return possible


def checkDesign(design, towels, unreachable):
    if len(design) == 0:
        return True

    # Memoization
    if design in unreachable:
        return False

    for towel in towels:
        towelLen = len(towel)

        if towelLen <= len(design) and design[:towelLen] == towel:
            if checkDesign(design[towelLen:], towels, unreachable):
                return True

    unreachable.add(design)
    return False
