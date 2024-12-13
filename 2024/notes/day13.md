# [Day 13 - Claw Contraption](https://adventofcode.com/2024/day/13)

> [<- Previous](day12.md) | [Next ->](day14.md)

Wow I'm really proud of this one. This was a math related one and was really easy to solve once you figured the trick. Could've had a much better time
if I realized I copied by input text incorrectly (or rather, should've formatted it slightly differently).

|                | Part A | Part B | Total |
| -------------- | :----: | :----: | :---: |
| Coding Time    | 49:46  |  1:55  | 51:41 |
| Execution Time |  < 0s  |  < 0s  | < 0s  |

## Part A

After reading through the problem and setting up some of the parsing, I decided to see if this was possible to solve linearly. I opened [desmos](https://www.desmos.com/calculator)
and decided to put in some variables and solve the linear equations, and I found a formula! (which I implemented into my code)

$$\text{Button pushes for A} = -\frac{B_y P_x - B_x P_y}{B_x A_y - B_y A_x}$$
$$\text{Button pushes for B} = \frac{P_x - A_xA}{B_x}$$

> [!TIP]
> As mentioned above, a trick to solving this is noticing that this is a system of linear equations.
> There are two variables to solve (button pushes for A and B) and two equations (for prize X and prize Y)
>
> The equations are:
>
> $$
> \begin{cases}
> P_x = A_x A + B_x B \\
> P_y = A_y A + B_y B
> \end{cases}
> $$
>
> Where $A$ = Number of A button pushes, $B$ = Number of B button pushes

I could have done this even faster, but I should have realized my parsing was slighting incorrect. I needed an empty line to add the `game` to the table.
Since the input didn't have a final empty line, my code was missing the last `game` and gave me an incorrect answer. Took me too long to figure that one out but I got it!

```python
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

```

## Part B

Really proud of this one. I usually don't know what Part B is going to offer, and this time was certainly no exception. However, it was a really quick change
and since I already did the hard work in Part A, and it worked flawlessly.

Could've saved even more time if I wasn't yapping about doing poorly on Part A, but I'm not going for time anyways this year!

```python
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
        Px = game[2][0] + 10000000000000
        Py = game[2][1] + 10000000000000

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

```

