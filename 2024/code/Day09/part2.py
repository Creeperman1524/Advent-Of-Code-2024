def solve(input):
    system = ""

    for line in input:
        system += line

    system = list(system)

    # Expands the filesystem
    expandedSystem = []
    fileBool = True
    fileId = 0
    for x in system:
        if fileBool:

            for _ in range(int(x)):
                expandedSystem.append(fileId)

            fileBool = False
            fileId += 1

        else:
            for _ in range(int(x)):
                expandedSystem.append(".")

            fileBool = True

    # Condenses the filesystem
    fileId -= 1

    start = 0
    startSize = 0
    end = len(expandedSystem) - 1
    endSize = 0

    while fileId >= 0:
        start = 0
        end = end - endSize
        startSize = 0
        endSize = 0

        # Move end
        while expandedSystem[end] != fileId:
            end -= 1

        # Expands the end window
        while expandedSystem[end - endSize] == fileId:
            endSize += 1

        fileId -= 1

        # Tries to find a spot for the group
        while start <= end:
            start = start + startSize
            startSize = 0

            # Move start
            while expandedSystem[start] != ".":
                start += 1

            if start > end:
                break

            # Expands the start window
            while expandedSystem[start + startSize] == ".":
                startSize += 1

            # Swaps the two windows if the end can fit into the start
            if endSize <= startSize:
                break

        if start > end:
            continue

        for x in range(endSize):
            expandedSystem[start + x] = expandedSystem[end - x]
            expandedSystem[end - x] = "."

    # Calculates the checksum for this condensed version
    checksum = 0

    for i in range(len(expandedSystem)):
        if expandedSystem[i] == ".":
            continue

        checksum += i * expandedSystem[i]

    return checksum
