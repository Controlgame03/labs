import random
import matplotlib.pyplot as plt

MAX_BITSET_SIZE = 15
FIRST_POLINOMIAL_SIZE = 2
SECOND_POLINOMIAL_SIZE = 5
THIRD_POLINOMIAL_SIZE = 11
SEED = 0  # time(0), 23, 34, 38, 192, 218, 245, 284, 322, 355, 356, 387


def Berlekamp_Massey_algorithm(sequence):
    N = len(sequence)
    s = sequence[:]

    for k in range(N):
        if s[k] == 1:
            break
    f = set([k + 1, 0])  # use a set to denote polynomial
    l = k + 1

    g = set([0])
    a = k
    b = 0

    for n in range(k + 1, N):
        d = 0
        for ele in f:
            d ^= s[ele + n - l]

        if d == 0:
            b += 1
        else:
            if 2 * l > n:
                f ^= set([a - b + ele for ele in g])
                b += 1
            else:
                temp = f.copy()
                f = set([b - a + ele for ele in f]) ^ g
                l = n + 1 - l
                g = temp
                a = b
                b = n - l + 1
    return l


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
    secondPolinomial = getBits("100101")
    thirdPolinomial = getBits("100000000101")

    lfsr1 = Lfsr(firstPolinomial, FIRST_POLINOMIAL_SIZE)  # x^2 + x + 1
    lfsr2 = Lfsr(secondPolinomial, SECOND_POLINOMIAL_SIZE)  # x^5 + x^2 + 1
    lfsr3 = Lfsr(thirdPolinomial, THIRD_POLINOMIAL_SIZE)  # x^11 + x^2 + 1

    limit = 100
    result = []
    print("lfsr ---> ", end="")
    for _ in range(limit):
        res1 = lfsr1.get_next()
        res2 = lfsr2.get_next()
        res3 = lfsr3.get_next()
        res = (res1 and res2) ^ (res2 and res3) ^ res3

        result.append(int(res))
        print(int(res), end=", ")
    print('\n')
    span = Berlekamp_Massey_algorithm(result)
    print('линейная сложность --> ', span)
    spans = []
    for i in range(1, limit):
        tmp = []
        for j in range(i):
            tmp.append(result[j])
        spans.append(Berlekamp_Massey_algorithm(tmp))
    arguments = []
    for i in range(1, 100):
        arguments.append(i)
    print(len(arguments))
    print(len(spans))
    plt.plot(arguments, spans)
    plt.xlabel('Количество бит')
    plt.ylabel('Линейная сложность')
    plt.show()
