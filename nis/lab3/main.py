import random
import sys
import numpy.random
import matplotlib.pyplot as plt

def getWorkingSystemNumber(arr, time, delta=0):
    count = 0
    for i in range(len(arr)):
        if arr[i] > time + delta:
            count += 1
    return count

def createGraphic(times, title):
    number_of_points = 100
    tm = times[len(times) - 200]
    t_step = tm / number_of_points
    delta_t = 0.1 * t_step

    arguments = []
    values = []
    lower_limit = times[0]
    upper_limit = tm

    for i in range(1, number_of_points):
        arguments.append(lower_limit + i * (upper_limit - lower_limit) / number_of_points)

    for i in range(len(arguments)):
        n_t = getWorkingSystemNumber(times, arguments[i])
        n_t_delta = getWorkingSystemNumber(times, arguments[i], delta_t)
        values.append((n_t - n_t_delta) / (n_t * delta_t))

    plt.plot(arguments, values)
    plt.title(title)
    plt.xlabel('t')
    plt.ylabel('lambda(t)')
    plt.show()

    values = []
    for i in range(len(arguments)):
        values.append((float)(getWorkingSystemNumber(times, arguments[i])/len(times)))

    plt.plot(arguments, values)
    plt.title(title)
    plt.xlabel('t')
    plt.ylabel('R(t)')
    plt.show()

def model1(k):
    tArray = []
    lambdaArray = [] 
    for i in range(k):
        lambdaArray.append(random.random())
    for i in range(N):
        id = random.randint(0, k - 1)
        tArray.append(numpy.random.exponential(1/lambdaArray[id]))
    tArray.sort()
    return tArray

def model2(n):
    tArray = []
    lambdaArray = []
    for i in range(n):
        lambdaArray.append(random.random())

    for i in range(N):
        t_i = sys.maxsize
        for i in range(n):
            tNew = numpy.random.exponential(1 / lambdaArray[i])

            if tNew < t_i:
                t_i = tNew

        tArray.append(t_i)
    tArray.sort()
    return tArray

def model3(n):
    tArray1 = []
    tArray2 = []
    lambdaArray = [] 
    for i in range(n):
        lambdaArray.append(random.random())

    for i in range(N):
        t_i_1 = 0 
        t_i_2 = 0
        for i in range(n):
            new_value = numpy.random.exponential(1 / lambdaArray[i])
            t_i_2 += numpy.random.exponential(1 / lambdaArray[i])
            if new_value > t_i_1:
                t_i_1 = new_value
        tArray1.append(t_i_1)
        tArray2.append(t_i_2)

    tArray1.sort()
    tArray2.sort()
    return tArray1, tArray2

N = 10000
k = int(input('number of subsitems: '))
createGraphic(model1(k), 'model1')
n = int(input('number of systems: '))
createGraphic(model2(n), 'model2')
tArray1, tArray2 = model3(n)
createGraphic(tArray1, 'model3.1')
createGraphic(tArray2, 'model3.2')