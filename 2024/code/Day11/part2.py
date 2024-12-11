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
