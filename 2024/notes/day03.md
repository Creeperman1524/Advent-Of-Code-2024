# [Day 3 - Mull It Over](https://adventofcode.com/2024/day/3)

> [<- Previous](day02.md) | [Next ->](day04.md)

REGEX!!! A really fun problem to show the power of regex (and how easy it can make problems!). Had to break out the [regex101](https://regex101.com/) website for this one.

|                | Part A | Part B | Total  |
| -------------- | :----: | :----: | :----: |
| Coding Time\*  |        | 34:28  |        |
| Execution Time |  < 0s  |  < 0s  | 0.001s |

> \*Time is not recorded as this day was started later rather than at midnight, so no accurate time for part 1 can be recorded

## Part A

This was as close as you can get to solving a question entirely with regex. It made this really quite simple.

> [!TIP]
> This could be further simplified with more regex to get each digit within the brackets (possibly using groups), but I felt the pythonic way made more sense in my head

```python
import re


def solve(input):
    total = 0

    for line in input:
        exprs = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", line)

        for expr in exprs:
            num1 = int(expr[4:-1].split(",")[0])
            num2 = int(expr[4:-1].split(",")[1])

            total += num1 * num2

    return total

```

## Part B

This one definitely started to stump me and I made many different errors throughout the process. I essentially wanted to section off the input into
blocks that can be ran with the same method as in part 1.

Remember to make sure your character counts are correct (and verify them if you aren't sure with the debugger!)

> [!TIP]
> A solution that I saw also used regex to automatically find these valid blocks by searching for the `do()` and `don't()` pairs.
> That might be a much neater solution than mine.

```python
import re


def solve(input):
    total = 0

    line = ""
    for x in input:
        line += x

    start = 0

    while start < len(line):
        end = re.search(r"don't\(\)", line[start:])
        if end != None:
            end = end.start() + start
        else:
            end = len(line)

        exprs = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", line[start:end])

        for expr in exprs:
            num1 = int(expr[4:-1].split(",")[0])
            num2 = int(expr[4:-1].split(",")[1])

            total += num1 * num2

        start = re.search(r"do\(\)", line[end:])
        if start != None:
            start = start.start() + end
        else:
            start = len(line)

    return total

```
