import random

MAX_BITSET_SIZE = 15
FIRST_POLINOMIAL_SIZE = 2
SECOND_POLINOMIAL_SIZE = 5
THIRD_POLINOMIAL_SIZE = 11
SEED = 0  # time(0), 23, 34, 38, 192, 218, 245, 284, 322, 355, 356, 387


class Lfsr:
    def __init__(self, m, s):
        self.mask = m
        self.values = [False] * MAX_BITSET_SIZE
        self.size = s
        self.mode = "notStarted"

    def get_next(self):
        if self.mode == "notStarted":
            self.initialize_lfrs()
            self.mode = "started"

        res = True if self.values[self.size - 1] else False

        tmp = [False] * MAX_BITSET_SIZE

        for i in range(self.size):
            tmp[i] = self.mask[i] & self.values[i]

        for i in range(1, self.size):
            tmp[0] = tmp[0] ^ tmp[i]

        self.values.pop()
        self.values.insert(0, tmp[0])

        return res

    def initialize_lfrs(self):
        random.seed(SEED)
        self.values = [bool(random.getrandbits(1)) for _ in range(self.size)]

def getBits(value):
    bit_array = []
    for i in value:
        bit_array.append(i == '1')

    return bit_array
if __name__ == "__main__":
    # степени многочленов 2, 5, 11
    firstPolinomial = getBits("111")
    secondPolinomial = getBits("101001")
    thirdPolinomial = getBits("101000000001")

    lfsr1 = Lfsr(firstPolinomial, FIRST_POLINOMIAL_SIZE)  # x^2 + x + 1
    lfsr2 = Lfsr(secondPolinomial, SECOND_POLINOMIAL_SIZE)  # x^5 + x^2 + 1
    lfsr3 = Lfsr(thirdPolinomial, THIRD_POLINOMIAL_SIZE)  # x^11 + x^2 + 1

    limit = 100
    print("lfsr ---> ", end="")
    for _ in range(limit):
        res1 = lfsr1.get_next()
        res2 = lfsr2.get_next()
        res3 = lfsr3.get_next()

        res = (res1 and res2) ^ (res2 and res3) ^ res3

        print(int(res), end=", ")
