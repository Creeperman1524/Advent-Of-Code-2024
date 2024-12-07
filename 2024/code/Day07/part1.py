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
