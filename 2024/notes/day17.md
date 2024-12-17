# [Day 17 - Chronospatial Computer](https://adventofcode.com/2024/day/17)

> [<- Previous](day16.md) | [Next ->](day18.md)

Well, I said yesterday that I wished there were more logic puzzles, and they certainly provided! I actually really enjoyed this one, especially Part B (although it took
painfull long to complete). A nice change of pace, almost remind me of Assembly coding!

|                | Part A | Part B  |  Total  |
| -------------- | :----: | :-----: | :-----: |
| Coding Time    | 23:41  | 2:04:50 | 2:28:31 |
| Execution Time |  < 0s  |  < 0s   |  < 0s   |

## Part A

Honestly this one really wasn't that bad. I think I spent more time writing comments and making the code look nice than actually solving the problem.

It is very self explanatory, simply just implementing each instruction as they are written and printing the output.

**Beware, another yap session ahead!**

```python
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

```

## Part B

Now this is something that I definitely did not expect to have for Part B. We have to find a value for the `A` register that returns the _same program used to create it_.

First, of course, I went the brute force way and created a loop to check every value of A. Of course, hindsight shows just how stupid this was (as the answer is somewhere in the `2^48` range!!)

So I decided it was time to get smarter, there must have been a pattern to my particular program that I can exploit. I wrote down all the opcodes and operands and translated it into
the functions I made (seen below.)

```
2 4 A % 8 => B
1 1 B ^ 1 => B
7 5 trunc(A / 2**B) => C
1 5 B ^ 5 => B
4 5 B^C => B
0 3 trunc(A / 2**3) => A // must be a power of 8
5 5 out B % 8
3 0 loop if A != 0

```

> Taken directly from my notes while working on Part B

Here, two things stood out to me. **A is divided by 8 each loop** and **keeps the program looping for as long as it's above 0**. This is important because it sets a bounds to how many times
the program loops. Since it prints a "byte" (I'm going to use byte to represent chunks of 3 bits for this problem) each loop, and my program contains 16 bytes, this sets `A` to be in the
realm of `8^16` (no chance of brute forcing here!).

Look at the problem further, and with a lot of mention of [bitwise operators](https://en.wikipedia.org/wiki/Bitwise_operation), I decided to start thinking in bits,
which came up with this logic:

```
B = A % 8   // bottom three bits
B ^= 1      // flips last bit
C = A >> B  // shifts A by B
B ^= 5      // flips 2nd and last bit
B ^= C      // flips all bits that match in C
B % 8       // bottom three bits
out B       // print last 3 bits
A = A >> 3  // shift A by 3
```

This gives clearer steps on how to reverse engineer this program. We need to find the 48 bits of `A` such that they go through this function and map to the output given by the program.

```
A
XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

output
 2   4   1   1   7   5   1   5   4   5   0   3   5   5   3   0
010 100 001 001 111 101 001 101 100 101 000 011 101 101 011 000
```

Okay, that got me somewhere, but I was still stuck on solving for the 48 bits. After fiddling around with trying some bit strings myself, I discovered that I should work _backwards_
in order to solve this. This is because of the pesky `C = A >> B`. When reversing the program, it relies on the bits before it (which we don't have yet!) to determine what to do with
the current bits. So, by working backwards, the `A` bit string will have no bytes that affect it due to all the bit shifts.

An example of this is:

To print the last bit (`000`), we only need to search for 8 values (`000` -> `111`) for `A` (or rather, the first byte of `A` out of the 16)

```js
    s     A%8    B^1   C=A>B   B^5    B^C
A: 001 -> 001 -> 001 -> 001 -> 001 -> 001
B: 000 -> 001 -> 000 -> 000 -> 101 -> 100 -> out
C: 000 -> 000 -> 000 -> 001 -> 001 -> 001

need: 000 != 001
```

Since `001` did not work, we move onto another byte

```js
    s     A%8    B^1   C=A>B   B^5    B^C
A: 100 -> 100 -> 100 -> 100 -> 100 -> 100
B: 000 -> 100 -> 101 -> 101 -> 000 -> 000 -> out
C: 000 -> 000 -> 000 -> 000 -> 000 -> 000

need: 000 = 000
```

`100` worked, so we know that A must be

```js
A
100 XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
```

Of course, as `A` grows larger, doing this by hand becomes a little combersome. So that is what I programmed! It is very hardcoded to my specific problem, but it worked (after some bug fixes)

My first attempt at this solution got me _mostly_ there, although the first 2 output bytes (last 2 when calculating) always seemed to be off and I could not understand why.

I eventually identified the problem as there being _multiple bytes which satisfy a current output_, which sucked because it might not be correct downstream and mess up those bytes.
I decided to fix this with backtracking, removing the incorrect byte and trying the next one. With this solution, it either worked or was impossible.

Overall pretty fun challenge that used a lot of brain power.

```python
def solve(input):
    solve = [2, 4, 1, 1, 7, 5, 1, 5, 4, 5, 0, 3, 5, 5, 3, 0]

    ansArr = []

    def findAnsArr(pointer):
        ans = calcA(ansArr)
        if pointer < 0:
            return

        for i in range(8):
            a = (ans >> (pointer * 3)) + i
            B = a % 8
            B ^= 1
            C = a >> B
            B ^= 5
            B ^= C
            B %= 8

            if solve[pointer] == B:
                # Adds on the found 3 bits
                ansArr.append(a % 8)
                findAnsArr(pointer - 1)

                # Didn't find the answer, try new byte
                if len(ansArr) != len(solve):
                    ansArr.pop()
                    continue

                return

    findAnsArr(15)

    return calcA(ansArr)


def calcA(ansArr):
    ans = 0
    for i in range(len(ansArr)):
        ans += ansArr[i] << (3 * (15 - i))

    return ans

```

