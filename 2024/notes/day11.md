# [Day 11 - Plutonian Pebbles](https://adventofcode.com/2024/day/11)

> [<- Previous](day10.md) | [Next ->](day12.md)

Started to get some [Outer Wilds](https://outerwilds.fandom.com/wiki/Quantum_Shards) vibes from this problem. O.o

This was a really fun problem that was easy in principle but definitely required some thinking. It finally put my brute forcing methods
to the test with Part B, which I was excited about because it made me think of a better solution.

|                | Part A | Part B | Total  |
| -------------- | :----: | :----: | :----: |
| Coding Time    | 13:12  | 17:13  | 30:43  |
| Execution Time | 0.132s | 0.049s | 0.181s |

## Part A

Probably as simple as it can get. Maybe the syntax can be condensed or done in a more "python" way, or evendone in a more efficient way (as can be seen in Part B)
but I am happy how it turned out and it worked first try too!

> [!TIP]
> I made sure to create a new array (`newStones`) while updating the `stones` array each blink, that way as I loop through the `stones` it would only caluclate
> the rules for a set amount of stones, rather than the continuously updating version

```python
def solve(input):
    blinks = 25

    inputStr = ""

    for line in input:
        inputStr += line

    stones = inputStr.split(" ")

    # Blinks
    for _ in range(blinks):

        # Runs the process on each stone
        newStones = list()
        for stone in stones:

            # Rule 1
            if stone == "0":
                newStones.append("1")

            # Rule 2
            elif len(stone) % 2 == 0:
                left = stone[: len(stone) // 2]
                right = stone[len(stone) // 2 :]

                # Convert to int and string to remove leading 0s
                newStones.append(str(int(left)))
                newStones.append(str(int(right)))

            # Rule 3
            else:
                newStones.append(str(int(stone) * 2024))

        stones = newStones

    return len(stones)

```

## Part B

Oh to see my reaction when Part B only contained 2 lines and all I _thought_ I had to do was change a single variable. I immediately thought
they would never make it that easy (I still tried it though, only got to 40 iterations before I gave up waiting).

I had a look back through the problem to think of other solutions, and saw some repeating patters such as `0 -> 1 -> 2024 -> 20, 24 -> 2, 0, 2, 4` -> etc.

I was thinking there must be a way to compute these only once and save the result for later. Hmmm, sounds a lot like memoization...

> [!TIP]
> My idea was to use a frequency dictionary to store the amount of each stone type we have.
>
> Since stones with the same number follow the same pattern, I just added the number of stones in the dictionary to how many new stones they add based on the rules
> (showcased with the `count` variable)

I definitely could have used `Counter` from the `collections` package again, but I don't have very much experience with it and felt I was confident enough in
implementing it myself. Although, I was a bit verbose with it and definitely could have used the package to condense my code.

I'm glad I thought of this solution so quickly, and it runs even faster than Part A does (with more iterations!)

```python
def solve(input):
    blinks = 75

    inputStr = ""

    for line in input:
        inputStr += line

    # Order doesn't matter, so we can use the repetition of certain patterns to our advantage
    stoneCounter = {}

    # Adds the initial state
    stones = inputStr.split(" ")

    for stone in stones:
        if stone in stoneCounter:
            stoneCounter[stone] += 1
        else:
            stoneCounter[stone] = 1

    # Blinks
    for _ in range(blinks):

        # Runs the process on each stone
        newStones = {}
        for stone, count in stoneCounter.items():

            # Rule 1
            if stone == "0":
                if "1" in newStones:
                    newStones["1"] += count
                else:
                    newStones["1"] = count

            # Rule 2
            elif len(stone) % 2 == 0:
                # Convert to int and string to remove leading 0s
                left = str(int(stone[: len(stone) // 2]))
                right = str(int(stone[len(stone) // 2 :]))

                if left in newStones:
                    newStones[left] += count
                else:
                    newStones[left] = count

                if right in newStones:
                    newStones[right] += count
                else:
                    newStones[right] = count

            # Rule 3
            else:
                new = str(int(stone) * 2024)
                if new in newStones:
                    newStones[new] += count
                else:
                    newStones[new] = count

        stoneCounter = newStones

    count = 0
    for c in stoneCounter.values():
        count += c

    return count

```
