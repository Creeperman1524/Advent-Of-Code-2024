# [Day 1 - Historian Hysteria](https://adventofcode.com/2024/day/1)

> ~~<- Previous~~ | [Next ->](day02.md)

A good start to this year! Seeing as this is my first "real" attempt at completing the year's advent, I decided to use Python for my solutions.
I am a bit rusty at it because I haven't used it much recently, but I quickly got into the swing of things.

I quickly set up a coding environment that I am happy with (as well as this repo) to quickly test and run my program, which I am for sure going to improve upon later.

|                | Part A | Part B | Total |
| -------------- | :----: | :----: | :---: |
| Coding Time\*  |        |  5:27  |       |
| Execution Time |  < 0s  |  < 0s  | < 0s  |

> \*Time is not recorded as this day was started later rather than at midnight, so no accurate time for part 1 can be recorded

## Part A

This is probably as straight forward as it can get, mostly trying to learn how the inputs are formatted for the questions and parsing through what I need.

```python
def solve(input):

    totalDistance = 0

    left = []
    right = []

    for line in input:
        left.append(line.split("   ")[0])
        right.append(line.split("   ")[1])

    left = sorted(left)
    right = sorted(right)

    for i in range(len(left)):
        totalDistance += abs(int(left[i]) - int(right[i]))

    return totalDistance

```

## Part B

Very similar to Part A, although I did want to try out the `Counter` from the `collections` library that can easily make a frequency array so I didn't have to do it myself.

```python
from collections import Counter


def solve(input):

    similarity = 0

    left = []
    right = []

    for line in input:
        left.append(line.split("   ")[0])
        right.append(line.split("   ")[1])

    c = Counter(right)

    for i in range(len(left)):
        similarity += int(left[i]) * c[left[i]]

    return similarity

```
