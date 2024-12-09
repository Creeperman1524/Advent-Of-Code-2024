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
    end = len(expandedSystem) - 1
    start = 0

    while start <= end:
        # Move start
        while expandedSystem[start] != ".":
            start += 1

        # Move end
        while expandedSystem[end] == ".":
            end -= 1

        if start > end:
            continue

        # Swap
        expandedSystem[start] = expandedSystem[end]
        expandedSystem[end] = "."

    # Calculates the checksum for this condensed version
    checksum = 0

    for i in range(len(expandedSystem)):
        if expandedSystem[i] == ".":
            continue

        checksum += i * expandedSystem[i]

    return checksum
