# [Day 7 - Bridge Repair](https://adventofcode.com/2024/day/7)

> [<- Previous](day06.md) | [Next ->](day08.md)

This one definitely stumped me in the beginning. I knew what had to be done but I was definitely too tired to fully understand
how to implement it. Nonetheless, I got it done!

This all boils down to creating every combination of operators and evaluating them to see if you can get the answer.

|                | Part A | Part B  |  Total  |
| -------------- | :----: | :-----: | :-----: |
| Coding Time\*  |        |  12:02  |         |
| Execution Time | 0.264s | 24.348s | 24.612s |

> \*Time is not recorded as this day was started later rather than at midnight, so no accurate time for part 1 can be recorded

## Part A

I did feel pretty smart about how I implemented this, using an integer's binary representation to keep track of what operators are being used.
Although this doesn't expand with more operators (which really sucked for Part B), I still got to have practice with bitwise operators such as `>>` and `&`

> [!TIP]
> A thing to note is that _all_ combinations will eventually need to be exhausted as an input could be deemed incorrect

```python
def solve(input):
    total = 0

    for line in input:
        ans = int(line.split(":")[0])
        nums = [int(k) for k in line.split(":")[1][1:].split(" ")]

        output = testEquation(nums, ans)
        if output != False:
            total += output

    return total


def testEquation(nums, ans):
    # Uses a binary int to represent the operators
    # 1101 = * * + *
    operators = 2 ** (len(nums) - 1) - 1

    # Iterators over all combinations of operators
    while operators >= 0:
        total = nums[0]

        # Extracts each bit and performs the operator
        for i in range(1, len(nums)):
            op = (operators >> (i - 1)) & 1

            if op == 0:  # +
                total += nums[i]
            elif op == 1:  # +
                total *= nums[i]

        # Found a solution, return early
        if total == ans:
            return ans

        operators -= 1

    return False

```

## Part B

This is where brute force started to really slow me down. Although still not bad time-wise, I could definitely feel the exponential growth with having a base
of 3 rather than 2. Basically the same thing as Part A, except I had to revert to using an array for keep tracking of the operator combinations.

It was ugly code, but it worked

> [!TIP]
> Another (more common, and likely better) solution I saw was performing a [DFS](https://en.wikipedia.org/wiki/Depth-first_search) with the combination of operators, which can
> generalize better than my method

```python
def solve(input):
    total = 0
    count = 0

    for line in input:
        ans = int(line.split(":")[0])
        nums = [int(k) for k in line.split(":")[1][1:].split(" ")]

        output = testEquation(nums, ans)
        if output != False:
            total += output

        count += 1

    return total


def testEquation(nums, ans):
    # Uses an array implementation for the operators
    # 1201 = * || + *

    totalCombo = 3 ** (len(nums) - 1)
    operators = [2 for _ in range(len(nums) - 1)]

    # Iterators over all combinations of operators
    while totalCombo >= 0:
        total = nums[0]

        # Extracts each bit and performs the operator
        for i in range(1, len(nums)):
            op = operators[i - 1]

            if op == 0:  # +
                total += nums[i]
            elif op == 1:  # +
                total *= nums[i]
            elif op == 2:  # ||
                total = int(str(total) + str(nums[i]))

        if total == ans:
            return ans

        totalCombo -= 1

        # Decrements each of the operators
        pointer = len(operators) - 1
        operators[pointer] -= 1

        # Ripples it down
        while operators[pointer] < 0:
            operators[pointer] = 2
            pointer -= 1
            operators[pointer] -= 1

    return False

```
