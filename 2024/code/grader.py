import datetime
import glob
import importlib.util
import os
import sys
import time

# Finds the directory based on the current day or program arguments
day = str(datetime.datetime.now().day)

if len(sys.argv) > 1:
    day = sys.argv[1]

# 0-Padding
if len(str(day)) < 2:
    day = "0" + str(day)

# Thanks ChatGPT
# This code is really fidelly but it works I guess
# FIX: Need a better solution for this
root_dir = os.path.dirname(os.path.abspath(__file__))
part1Path = os.path.join(root_dir, f"Day{day}", "part1.py")
part2Path = os.path.join(root_dir, f"Day{day}", "part2.py")


# Function to dynamically import a module
def import_part(script_path):
    if os.path.exists(script_path):
        module_name = os.path.basename(script_path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        print(f"Error: {script_path} not found!")
        exit(1)
        return None


part1 = import_part(part1Path)
part2 = import_part(part2Path)
solve1 = part1.solve
solve2 = part2.solve

print(f"Running program for Day {day}\n")

# Handling for the test case(s)
caseInput = list()

for caseFile in glob.glob(f"./Day{day}/case1*.txt"):
    with open(caseFile, "r") as f:
        for line in f:
            caseInput.append(line.rstrip())

    print(f"{caseFile.split('/')[2][:-4]}: {solve1(caseInput)}")
    caseInput = list()

for caseFile in glob.glob(f"./Day{day}/case2*.txt"):
    with open(caseFile, "r") as f:
        for line in f:
            caseInput.append(line.rstrip())

    print(f"{caseFile.split('/')[2][:-4]}: {solve2(caseInput)}")
    caseInput = list()

# Handling for the solution
fileInput = list()

with open(f"./Day{day}/input1.txt", "r") as f:
    for line in f:
        fileInput.append(line.rstrip())

print(f"Part 1: {solve1(fileInput)}")

fileInput = list()

with open(f"./Day{day}/input2.txt", "r") as f:
    for line in f:
        fileInput.append(line.rstrip())

print(f"Part 2: {solve2(fileInput)}\n")

# Timing
times = 5

# Gets the first input
fileInput = list()

with open(f"./Day{day}/input1.txt", "r") as f:
    for line in f:
        fileInput.append(line.rstrip())

# Times it
total1 = 0.0
answer1 = ""

print("Timing Part 1...")

for i in range(times):
    start1 = time.time()
    answer = solve1(fileInput)
    end1 = time.time()
    total1 += end1 - start1

    print(f"{i + 1} / {times}")
    sys.stdout.write("\033[F")

print(f"Completed in {round(total1 / times, 3)}s averaged over {times} tries")

fileInput = list()

with open(f"./Day{day}/input2.txt", "r") as f:
    for line in f:
        fileInput.append(line.rstrip())

print("Timing Part 2...")

# Times it
total2 = 0.0
answer2 = ""

for i in range(times):
    start2 = time.time()
    answer = solve2(fileInput)
    end2 = time.time()
    total2 += end2 - start2

    print(f"{i + 1} / {times}")
    sys.stdout.write("\033[F")

print(f"Completed in {round(total2 / times, 3)}s averaged over {times} tries\n")

print(f"Total: {round((total1 + total2) / 5, 3)}s")
