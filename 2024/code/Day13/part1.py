def solve(input):
    games = []

    # Parses the games
    game = []
    for i in range(len(input)):
        line = input[i]

        if i % 4 == 0 or i % 4 == 1:
            # Button A and B
            x = int(line.split("+")[1].split(",")[0])
            y = int(line.split("+")[2])
            game.append((x, y))

        elif i % 4 == 2:
            # Prize
            x = int(line.split("=")[1].split(",")[0])
            y = int(line.split("=")[2])
            game.append((x, y))

        elif i % 4 == 3:
            # Space
            games.append(game)
            game = []

    totalTokens = 0
    for game in games:
        Ax = game[0][0]
        Ay = game[0][1]
        Bx = game[1][0]
        By = game[1][1]
        Px = game[2][0]
        Py = game[2][1]

        A = findAButton(Ax, Ay, Bx, By, Px, Py)
        B = (Px - (Ax * A)) / Bx

        # Checks if A is an integer
        if A % 1 != 0 or B % 1 != 0:
            continue

        totalTokens += int((A * 3) + B)

    return totalTokens


# Returns the amount of times to press button A
# Found this by solving the system of equations (by hand)
def findAButton(Ax, Ay, Bx, By, Px, Py):
    return -(By * Px - Bx * Py) / (Bx * Ay - By * Ax)
