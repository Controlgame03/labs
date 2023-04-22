import matplotlib.pyplot as plt


def removeZeros(vector):
    while len(vector) != 0 and vector[0] == 0:
        vector.pop(0)

    return vector


def modC(c, g):
    c = removeZeros(c)
    g = removeZeros(g)
    sizeC = len(c)
    sizeG = len(g)
    while sizeC >= sizeG:
        for i in range(sizeG):
            c[i] = (c[i] + g[i]) % 2
        c = removeZeros(c)
        sizeC = len(c)
        sizeG = len(g)

    return c


def code(c, moduleC):
    sizeC = len(c)
    sizeModuleC = len(moduleC)
    a = c.copy()
    for i in range(sizeModuleC):
        a[sizeC - sizeModuleC + i] = moduleC[i]

    return a


def createMessages(n):
    if n == 0:
        return [[]]
    else:
        subCombinations = createMessages(n - 1)
        result = []
        for combination in subCombinations:
            result.append(combination + [0])
            result.append(combination + [1])
        return result


def getCodingList(messageList, g, n):
    codingList = []
    for m in messageList:
        if len(m) == 0:
            continue
        print('m => ', m)
        c = m.copy()

        for i in range(r - 1):
            c.append(0)

        moduleC = modC(c.copy(), g)
        a = code(c, moduleC)
        diff = n - len(a)
        for i in range(diff):
            a.insert(0, 0)
        codingList.append(a)
        print('a => ', a)
        print('------------------------------')

    return codingList


def getFactorial(num):
    factorial = 1

    for i in range(2, num + 1):
        factorial *= i
    return factorial


def getCoeff(k, n):
    return getFactorial(n) / (getFactorial(k) * getFactorial(n - k))


def getWeight(vector):
    sum = 0
    for i in vector:
        if i == 1:
            sum = sum + 1

    return sum


def getText(a):
    result = 'g(x) = '
    for i in range(len(a)):
        if a[i] == 0: continue
        degree = (len(a) - i - 1)
        if degree == 0:
            result = result + '1'
        else:
            result = result + 'x^' + str(degree) + ' + '

    return result


gList = [
    [1, 1, 0, 1]
    # [1, 0, 1, 1],
    # [1, 1, 1, 0, 1],
    # [1, 0, 1, 1, 1]
]

k = 4

for g in gList:
    l = 3
    plt.figure()
    plt.xlabel("Вероятность ошибки в канале")
    plt.ylabel("Вероятность ошибки декодирования")
    plt.title(getText(g) + ', k = ' + str(k))
    legends = []
    lStep = 1
    lAmount = 3
    for tL in range(lAmount):

        r = len(g)
        n = l + r - 1
        messageList = createMessages(l)
        codingList = getCodingList(messageList, g, n)

        condingSize = len(codingList)
        d = n
        weightToAmount = {}
        for a in range(condingSize):
            weight = getWeight(codingList[a])
            amount = weightToAmount.get(weight)
            amount = 1 if amount == None else amount + 1
            weightToAmount[weight] = amount
            for subA in range(a + 1, condingSize):
                minDiff = 0
                for i in range(n):
                    if (codingList[a][i] != codingList[subA][i]):
                        minDiff = minDiff + 1
                d = d if minDiff > d else minDiff

        print('distance : ', d)

        pErrors = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        pErrorsFinal = []
        pErrorsMax = []
        for p in pErrors:
            maxPr = 0
            for i in range(d):
                maxPr = maxPr + getCoeff(i, n) * (p ** i) * ((1 - p) ** (n - i))
            maxPr = 1 - maxPr
            pErrorsMax.append(maxPr)
            pError = 0
            for i in range(d, n + 1):
                amount = weightToAmount.get(i)
                amount = 0 if amount == None else amount
                pError = pError + amount * (p ** i) * ((1 - p) ** (n - i))

            pErrorsFinal.append(pError)
        plt.plot(pErrors, pErrorsFinal)
        plt.plot(pErrors, pErrorsMax)
        legends.append('Точная вероятность ошибки для l = ' + str(l))
        legends.append('Максимальная вероятность ошибки для l = ' + str(l))
        l = l + lStep

    plt.legend(legends, loc="upper left")
    plt.show()
