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
