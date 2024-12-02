def solve(input):
    safeCount = 0

    for report in input:
        levels = report.split(" ")

        increasing = int(levels[0]) < int(levels[1])

        safe = True
        for i in range(len(levels) - 1):
            if not safe:
                continue

            diff = abs(int(levels[i + 1]) - int(levels[i]))

            if int(levels[i]) >= int(levels[i + 1]) and increasing:
                safe = False

            if int(levels[i]) <= int(levels[i + 1]) and not increasing:
                safe = False

            if not (1 <= diff <= 3):
                safe = False

        if safe:
            safeCount += 1

    return safeCount
