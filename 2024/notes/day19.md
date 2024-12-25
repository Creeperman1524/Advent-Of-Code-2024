# [Day 19 - Linen Layout](https://adventofcode.com/2024/day/19)

> [<- Previous](day18.md) | [Next ->](day20.md)

I'm back!! A couple days later (currently writing this on Christmas Eve), but I have Day 19! This one was definitely a pretty easy on, although I still managed to struggle for not
understanding something correct. Still, a fun one to figure out!

|                | Part A | Part B | Total  |
| -------------- | :----: | :----: | :----: |
| Coding Time\*  |        |        |        |
| Execution Time | 0.246s | 0.625s | 0.871s |

> \*Time is not recorded as this day was started on a different day. I tried to self time but forgot to record some things. Generally, Part B was pretty quick but Part A took some time

## Part A

A little disappointed that it took me so long to complete this one (although you can't see the exact time, whoops). I basically had this format of code for most of the time, but
it seems to constantly get stuck my third test case (which was impossible). I tried adding memoization, but that still didn't seem to fix it.

After going to a party and taking some time off of the problem, I decided to look at the output of the designs it was trying to solve. I decided to flip the memoization to save
all the designs that did _not_ have a solution, which fixed my issue perfectly.

> [!TIP]
> Memoization is your friend!! Brute force can only take you so far, but once there's a lot of repetition, remembering previous outputs can start doing you some good

```python
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

```

## Part B

I think I'm starting to get good at these problems. I felt so much joy seeing that the Part B puzzle was the one I was thinking about in my head. Counting _all_ solutions is
a bit trickier than Part A, but I knew of a quick way to solve this. Instead of short circuiting the function with the `return`, I can easily just keep track of the different
ways to get the solution each recursion level and add them all together.

Of course, that would have taken forever as there is so many repeted designs, so adding a quick memoization table to keep track of the designs (even across multiple problems! I don't know much
that helped though) solved it in under a second. Don't you love computers??

> [!TIP]
> Like Part A, memoization will do wonders when brute forcing as it can save your computer from doing a lot of repetited calculations.

```python
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

    ways = 0
    counter = 0

    reachable = {}
    for design in designs:
        counter += 1
        # print(counter, design)
        ways += checkDesign(design, towels, reachable)

    return ways


def checkDesign(design, towels, reachable):
    if len(design) == 0:
        return 1

    if design in reachable:
        return reachable[design]

    ways = 0
    for towel in towels:
        towelLen = len(towel)

        if towelLen <= len(design) and design[:towelLen] == towel:
            ways += checkDesign(design[towelLen:], towels, reachable)

    reachable[design] = ways

    return ways

```

