# [Day 2 - Red-Nosed Reports](https://adventofcode.com/2024/day/2)

> [<- Previous](day01.md) | [Next ->](day03.md)

The day of status code 500 errors, it seems the Advent of Code server was struggling a bit. Still, a fairly easy problem although it took me some time
to figure out how to code it up.

|                | Part A | Part B |  Total  |
| -------------- | :----: | :----: | :-----: |
| Coding Time\*  | 52:18  | 28:32  | 1:20:50 |
| Execution Time | 0.002s | 0.005s | 0.007s  |

> \*These times might not completely correct as the 500 status code errors prevented me from viewing the problem right at midnight

## Part A

I made a few mistakes that costed me a lot of time (and sanity), mostly forgetting to include some `int()`s, which messed up a lot of the math.

```python
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

```

## Part B

Good ol' brute force, and it was pretty quick too. I can't see a smarter way of solving this, although I haven't given it much thought. Simply
removing one at a time and checking if it's valid was all that it took for the answer.

```python
def solve(input):
    safeCount = 0

    for report in input:
        levels = report.split(" ")

        if findSafe(levels):
            safeCount += 1
            continue

        for i in range(len(levels)):
            newLevel = levels.copy()
            newLevel.pop(i)
            if findSafe(newLevel):
                safeCount += 1
                break

    return safeCount


def findSafe(levels):
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

    return safe

```
