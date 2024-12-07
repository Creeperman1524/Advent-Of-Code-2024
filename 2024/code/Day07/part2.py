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
        # print(f"{count} / {len(input)}")

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
