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
