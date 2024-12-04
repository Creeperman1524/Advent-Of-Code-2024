import glob

from part1 import solve as solve1
from part2 import solve as solve2

# Handling for the test case(s)
caseInput = list()

for caseFile in glob.glob("./case1*.txt"):
    with open(caseFile, "r") as f:
        for line in f:
            caseInput.append(line.rstrip())

    print(f"{caseFile.split('/')[1][:-4]}: {solve1(caseInput)}")
    caseInput = list()

for caseFile in glob.glob("./case2*.txt"):
    with open(caseFile, "r") as f:
        for line in f:
            caseInput.append(line.rstrip())

    print(f"{caseFile.split('/')[1][:-4]}: {solve2(caseInput)}")
    caseInput = list()

# Handling for the solution
fileInput = list()

with open("./input1.txt", "r") as f:
    for line in f:
        fileInput.append(line.rstrip())

print(f"Part 1: {solve1(fileInput)}")

fileInput = list()

with open("./input2.txt", "r") as f:
    for line in f:
        fileInput.append(line.rstrip())

print(f"Part 2: {solve2(fileInput)}")
