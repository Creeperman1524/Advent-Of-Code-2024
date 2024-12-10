# [Day 9 - Disk Fragmenter](https://adventofcode.com/2024/day/9)

> [<- Previous](day08.md) | [Next ->](day10.md)

This one was fun to do because it was almost like 3 smaller problems smashed into one.
There was the parsing (or expanding, as I called it) of the file system, the condensing part,
which different between Part A and Part B, and then the checksum finale.

Overall, although definitely not optimal, I feel my solutions worked perfectly.

|                | Part A | Part B  |  Total  |
| -------------- | :----: | :-----: | :-----: |
| Coding Time\*  |        |  35:28  |         |
| Execution Time | 0.023s | 14.423s | 14.446s |

> \*Time is not recorded as this day was started later rather than at midnight, so no accurate time for part 1 can be recorded

## Part A

The condensing part reminded me a lot of [quick sort](https://en.wikipedia.org/wiki/Quicksort), where you have to swap elements depending on a pivot. In this case, it's using two pointers to swap
elements from the right side into the empty spaces on the left side.

```python
def solve(input):
    system = ""

    for line in input:
        system += line

    system = list(system)

    # Expands the filesystem
    expandedSystem = []
    fileBool = True
    fileId = 0
    for x in system:
        if fileBool:

            for _ in range(int(x)):
                expandedSystem.append(fileId)

            fileBool = False
            fileId += 1

        else:
            for _ in range(int(x)):
                expandedSystem.append(".")

            fileBool = True

    # Condenses the filesystem
    end = len(expandedSystem) - 1
    start = 0

    while start <= end:
        # Move start
        while expandedSystem[start] != ".":
            start += 1

        # Move end
        while expandedSystem[end] == ".":
            end -= 1

        if start > end:
            continue

        # Swap
        expandedSystem[start] = expandedSystem[end]
        expandedSystem[end] = "."

    # Calculates the checksum for this condensed version
    checksum = 0

    for i in range(len(expandedSystem)):
        if expandedSystem[i] == ".":
            continue

        checksum += i * expandedSystem[i]

    return checksum

```

## Part B

I feel this is also a pretty good soluion, although maybe it can be condensed with some more python syntax.

It expands on the two pointer solution from Part A and rather creates a window for both the start and end, searching for a
possible start window that the end window can fit into.

> [!TIP]
> One thing to look at for is that you should _only move each of the files once_.
>
> I made the mistake in not keeping track which files I moved originally, leading to the program trying to move the files multiple times as the pointer
> reaches them again

```python
def solve(input):
    system = ""

    for line in input:
        system += line

    system = list(system)

    # Expands the filesystem
    expandedSystem = []
    fileBool = True
    fileId = 0
    for x in system:
        if fileBool:

            for _ in range(int(x)):
                expandedSystem.append(fileId)

            fileBool = False
            fileId += 1

        else:
            for _ in range(int(x)):
                expandedSystem.append(".")

            fileBool = True

    # Condenses the filesystem
    fileId -= 1

    start = 0
    startSize = 0
    end = len(expandedSystem) - 1
    endSize = 0

    while fileId >= 0:
        start = 0
        end = end - endSize
        startSize = 0
        endSize = 0

        # Move end
        while expandedSystem[end] != fileId:
            end -= 1

        # Expands the end window
        while expandedSystem[end - endSize] == fileId:
            endSize += 1

        fileId -= 1

        # Tries to find a spot for the group
        while start <= end:
            start = start + startSize
            startSize = 0

            # Move start
            while expandedSystem[start] != ".":
                start += 1

            if start > end:
                break

            # Expands the start window
            while expandedSystem[start + startSize] == ".":
                startSize += 1

            # Swaps the two windows if the end can fit into the start
            if endSize <= startSize:
                break

        if start > end:
            continue

        for x in range(endSize):
            expandedSystem[start + x] = expandedSystem[end - x]
            expandedSystem[end - x] = "."

    # Calculates the checksum for this condensed version
    checksum = 0

    for i in range(len(expandedSystem)):
        if expandedSystem[i] == ".":
            continue

        checksum += i * expandedSystem[i]

    return checksum

```
