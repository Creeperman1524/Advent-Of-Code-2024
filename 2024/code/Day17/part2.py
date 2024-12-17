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
