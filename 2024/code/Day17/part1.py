import math


def solve(input):
    # Registers
    A = 0
    B = 0
    C = 0

    program = []
    pointer = 0

    # Parse the program
    for line in input:
        if "A" in line:
            A = int(line.split(" ")[2])
        elif "B" in line:
            B = int(line.split(" ")[2])
        elif "C" in line:
            C = int(line.split(" ")[2])
        elif "Program" in line:
            program = list(map(int, line[9:].split(",")))

    # Run the program
    output = ""
    while pointer < len(program):
        opcode = program[pointer]
        pointer += 1
        operand = program[pointer]
        pointer += 1

        combo = 0
        if operand >= 0 and operand <= 3:
            combo = operand
        elif operand == 4:
            combo = A
        elif operand == 5:
            combo = B
        elif operand == 6:
            combo = C

        match opcode:
            case 0:  # adv: trunc(A / combo) => A
                A = math.trunc(A / 2**combo)
            case 1:  # bxl: B ^ literal => B
                B = B ^ operand
            case 2:  # bst: combo % 8 => B
                B = combo % 8
            case 3:  # jnz: A != 0, pointer = literal (not increased after)
                if A != 0:
                    pointer = operand
            case 4:  # bxc: B ^ C => B (reads operand but does nothing)
                B = B ^ C
            case 5:  # out: combo % 8 => comma separated output
                output += str(combo % 8) + ","
            case 6:  # bdv: truc(A / combo) => B
                B = math.trunc(A / 2**combo)
            case 7:  # cdv: trunc(A / combo) => C
                C = math.trunc(A / 2**combo)

    output = output[:-1]
    return output
