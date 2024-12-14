def solve(input):
    robots = []

    sizex = 101
    sizey = 103

    # Parses the robots
    for line in input:
        Px = int(line.split("=")[1].split(",")[0])
        Py = int(line.split(",")[1].split(" ")[0])
        Vx = int(line.split("=")[2].split(",")[0])
        Vy = int(line.split(",")[2])
        robots.append([[Px, Py], [Vx, Vy]])

    # Runs the simulation for 100 seconds
    for _ in range(100):
        # Updates the robots
        for robot in robots:
            robot[0][0] += robot[1][0]
            robot[0][1] += robot[1][1]

            if robot[0][0] >= sizex or robot[0][0] < 0:
                robot[0][0] %= sizex

            if robot[0][1] >= sizey or robot[0][1] < 0:
                robot[0][1] %= sizey

    # Calculates the "safest area metric"
    quads = [0, 0, 0, 0]
    for robot in robots:
        # Ignore robots in the middle
        if robot[0][0] == sizex // 2 or robot[0][1] == sizey // 2:
            continue

        if (robot[0][0] < sizex // 2) and (robot[0][1] < sizey // 2):
            quads[0] += 1
        elif (robot[0][0] < sizex // 2) and (robot[0][1] > sizey // 2):
            quads[1] += 1
        elif (robot[0][0] > sizex // 2) and (robot[0][1] < sizey // 2):
            quads[2] += 1
        elif (robot[0][0] > sizex // 2) and (robot[0][1] > sizey // 2):
            quads[3] += 1

    safetyFactor = 1
    for q in quads:
        safetyFactor *= q

    return safetyFactor
