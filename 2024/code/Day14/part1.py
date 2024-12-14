def solve(input):
    quads = [0, 0, 0, 0]

    sizex = 101
    sizey = 103
    steps = 100

    # Parses the robots and find the quadrant they end up in
    for line in input:
        Px = int(line.split("=")[1].split(",")[0])
        Py = int(line.split(",")[1].split(" ")[0])
        Vx = int(line.split("=")[2].split(",")[0])
        Vy = int(line.split(",")[2])

        X = (Px + Vx * steps) % sizex
        Y = (Py + Vy * steps) % sizey

        # Calculates the "safest area metric"
        if X < sizex // 2 and Y < sizey // 2:
            quads[0] += 1
        elif X < sizex // 2 and Y > sizey // 2:
            quads[1] += 1
        elif X > sizex // 2 and Y < sizey // 2:
            quads[2] += 1
        elif X > sizex // 2 and Y > sizey // 2:
            quads[3] += 1

    safetyFactor = 1
    for q in quads:
        safetyFactor *= q

    return safetyFactor
