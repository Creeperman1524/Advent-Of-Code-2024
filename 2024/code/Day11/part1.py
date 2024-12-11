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
