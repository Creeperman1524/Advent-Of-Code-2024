from PIL import Image


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

    iterations = 0
    c = True
    while c:
        iterations += 1
        positions = set()

        # Updates the robots
        for robot in robots:
            robot[0][0] += robot[1][0]
            robot[0][1] += robot[1][1]

            if robot[0][0] >= sizex or robot[0][0] < 0:
                robot[0][0] %= sizex

            if robot[0][1] >= sizey or robot[0][1] < 0:
                robot[0][1] %= sizey

            positions.add((robot[0][0], robot[0][1]))

        # Find a christmas tree?
        # Detect when the robots are all in unique positions, most chance to create an image?
        if len(positions) == len(robots):
            c = False
            # display(sizex, sizey, positions, iterations)
            break

    return iterations


def display(sizex, sizey, positions, i):
    image = Image.new("RGB", (sizex, sizey), 0)
    for y in range(sizey):
        for x in range(sizex):
            if (x, y) in positions:
                image.putpixel((x, y), (5, 71, 42))

    image.save(f"output{i}.png")
