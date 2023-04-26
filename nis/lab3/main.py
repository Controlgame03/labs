import random
import numpy.random
import matplotlib.pyplot as plt
import math

pArray = [0.2, 0.8]
lambdaArray = [1.2, 1.4] 

def getWorkingSystemNumber(arr, time, delta=0):
    count = 0
    for i in range(len(arr)):
        if arr[i] > time + delta:
            count += 1
    return count

def getPracticalLambda(arguments, times, delta_t):
    values = []
    for i in range(len(arguments)):
        n_t = getWorkingSystemNumber(times, arguments[i])
        n_t_delta = getWorkingSystemNumber(times, arguments[i], delta_t)
        values.append((n_t - n_t_delta) / (n_t * delta_t))
    return values

def getTheoryLambdaResults(arguments, mode):
    values = []
    for i in arguments:
        result = 0
        if (mode == 1):
            temp1 = 0
            temp2 = 0
            for j in range(len(lambdaArray)):
                temp1 += math.exp(-lambdaArray[j] * i) * pArray[j]
                temp2 += lambdaArray[j] * math.exp(-lambdaArray[j] * i) * pArray[j]
            result = temp2 / temp1
        elif mode == 2:
            result = sum(lambdaArray)
        elif mode == 3:
            temp1 = 1 - (1 - math.exp(-lambdaArray[0] * i)) * (1 - math.exp(-lambdaArray[1] * i))
            temp2 = lambdaArray[0] * math.exp(-lambdaArray[0] * i) + lambdaArray[1] * math.exp(-lambdaArray[1] * i) - (lambdaArray[0] + lambdaArray[1]) * math.exp(-(lambdaArray[0] + lambdaArray[1]) * i)
            result = temp2 / temp1
        values.append(result)
    return values

def getPracticalR(arguments, times):
    values = []
    for i in range(len(arguments)):
        values.append((float)(getWorkingSystemNumber(times, arguments[i])/len(times)))
    
    return values

def getTheoryR(arguments, mode):
    values = []
    for i in arguments:
        result = 0
        if (mode == 1):
            for j in range(len(lambdaArray)):
                result += math.exp(-lambdaArray[j] * i) * pArray[j]
        elif mode == 2:
            result =  math.exp(-lambdaArray[0] * i) * math.exp(-lambdaArray[1] * i)
        elif mode == 3:
            result = 1 - (1 - math.exp(-lambdaArray[0] * i)) * (1 - math.exp(-lambdaArray[1] * i))
        values.append(result)
        
    return values

def createGraphic(times, title, mode):
    number_of_points = 100
    tm = times[len(times) - 200]
    t_step = tm / number_of_points
    delta_t = 0.1 * t_step

    arguments = []
    lower_limit = times[0]
    upper_limit = tm

    for i in range(1, number_of_points):
        arguments.append(lower_limit + i * (upper_limit - lower_limit) / number_of_points)
        
    plt.plot(arguments, getPracticalLambda(arguments, times, delta_t), label='practical')
    plt.plot(arguments, getTheoryLambdaResults(arguments, mode), label='theory')
    plt.legend()
    plt.title(title)
    plt.xlabel('t')
    plt.ylabel('lambda(t)')
    plt.show()

    plt.plot(arguments, getPracticalR(arguments, times), label='practical')
    plt.plot(arguments, getTheoryR(arguments, mode), label='theory')
    plt.legend()
    plt.title(title)
    plt.xlabel('t')
    plt.ylabel('R(t)')
    plt.show()

def model1():
    tArray = []
    
    for i in range(N):
        id = random.randint(0, len(pArray) - 1)
        tArray.append(numpy.random.exponential(1/lambdaArray[id]))
    tArray.sort()
    return tArray

def model2():
    tArray = []

    for i in range(N):
        temp1 = numpy.random.exponential(1 / lambdaArray[0])
        temp2 = numpy.random.exponential(1 / lambdaArray[1])
        tArray.append(min(temp1, temp2))
    tArray.sort()
    return tArray

def model3():
    tArray1 = []

    for i in range(N):
        t_i_1 = 0 
        t_i_2 = 0
        for i in range(len(lambdaArray)):
            new_value = numpy.random.exponential(1 / lambdaArray[i])
            t_i_2 += numpy.random.exponential(1 / lambdaArray[i])
            if new_value > t_i_1:
                t_i_1 = new_value
        tArray1.append(t_i_1)

    tArray1.sort()

    return tArray1

N = 10000
createGraphic(model1(), 'model1', 1)
createGraphic(model2(), 'model2', 2)
tArray1 = model3()
createGraphic(tArray1, 'model3', 3)