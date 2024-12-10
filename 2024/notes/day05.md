# [Day 5 - Print Queue](https://adventofcode.com/2024/day/5)

> [<- Previous](day04.md) | [Next ->](day06.md)

An interesting problem that I'm really proud of to think of a (decently) intelligent solution to.
My lack of experience in python definitely shows at times, as I'm sure there's much more efficient/concise
ways to write some things that I have.

|                | Part A | Part B |  Total  |
| -------------- | :----: | :----: | :-----: |
| Coding Time    | 55:20  | 21:22  | 1:16:42 |
| Execution Time | 0.034s | 0.076s | 0.111s  |

## Part A

Essentially does what the problem asks of it, creates structures to hold the rules and the pages, checks each page, and gives the total that it wants.

```python
def solve(input):
    parseRules = True
    rules = []
    pages = []

    # Parses the rules and pages
    for i in range(len(input)):
        line = input[i]

        # Divider
        if len(line) == 0:
            parseRules = False
            continue

        if parseRules:
            rules.append(line.split("|"))
        else:
            pages.append(line.split(","))

    total = 0

    for update in pages:
        # update = current edition we are looking at

        valid = True
        # Tries all the rules for this edition
        for rule in rules:

            # Checks if the rule is valid for this update
            if rule[0] in update and rule[1] in update:
                if update.index(rule[0]) > update.index(rule[1]):
                    valid = False

        if valid:
            # Adds the middle value
            total += int(update[len(update) // 2])

    return total

```

## Part B

At first, I wanted to do a combinatoric solution, brute forcing all possible arrangements of the pages and checking them against their ruleset.
Then I realized just how bad this idea would be (a single problem would sometimes require 22! different arrangements to be checked).

After taking a quick break and thinking it through, I thought of the idea to continually swap incorrect pairs of pages and eventually it _hopefully_ converges to a solved state.

> [!TIP]
> My thought process was that there _must_ be a solved state for all of the pages, as that is how the problem defined it as.
>
> Trying my idea of "swapping all incorrect pairs of pages until its solved" either would lead to the solution or an infinite cycle, which thankfully it gave me the correct answer

```python
def solve(input):
    parseRules = True
    rules = []
    pages = []

    # Parses the rules and pages
    for i in range(len(input)):
        line = input[i]

        # Divider
        if len(line) == 0:
            parseRules = False
            continue

        if parseRules:
            rules.append(line.split("|"))
        else:
            pages.append(line.split(","))

    total = 0

    for update in pages:
        # update = current edition we are looking at

        valid = validate(update, rules)

        # Ignore correct ones
        if valid:
            continue

        # Keep swapping incorrect rules until a solved state is found
        while not validate(update, rules):
            for rule in rules:
                if rule[0] in update and rule[1] in update:
                    if update.index(rule[0]) > update.index(rule[1]):
                        # Swaps the two numbers
                        update[update.index(rule[0])], update[update.index(rule[1])] = (
                            update[update.index(rule[1])],
                            update[update.index(rule[0])],
                        )
                        pass

        total += int(update[len(update) // 2])

    return total


def validate(update, rules):
    # Tries all the rules for this edition
    for rule in rules:

        # Checks if the rule is valid for this update
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]):
                return False

    return True

```
