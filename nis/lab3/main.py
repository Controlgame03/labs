import random
import sys
import numpy.random
import matplotlib.pyplot as plt
import math

# еще нужно сделать:
# 1. достроить теоретические графики надёжности с графики функц. над. для 3-ёх периодов
# 2. достроить теоретические графики интенсивности для 3-ёх периодов
def workable_systems(arr, time, delta=0):
    count = 0
    for i in range(len(arr)):
        if arr[i] > time + delta:
            count += 1
    return count

def printGraph(times, title, mode=1):
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
        n_t = workable_systems(times, arguments[i])
        n_t_delta = workable_systems(times, arguments[i], delta_t)
        values.append((n_t - n_t_delta) / (n_t * delta_t))

    #грфик интенсивности
    plt.plot(arguments, values)
    plt.title(title)
    plt.xlabel('Значения t')
    plt.ylabel('Значения lambda(t)')
    plt.show()

    #график надёжности
    values = []
    for i in range(len(arguments)):
        values.append((float)(workable_systems(times, arguments[i])/len(times)))

    plt.plot(arguments, values)
    plt.title(title)
    plt.xlabel('Значения t')
    plt.ylabel('Значения p(t)')
    plt.show()
def model1(n, k):
    times1 = []
    scale1 = []  # параметр обратный alpha
    for i in range(k):
        scale1.append(1 / random.random())
    for i in range(N):
        times1.append(numpy.random.exponential(scale1[math.floor(random.random() * k)]))
    times1.sort()
    return times1
def model2(n):
    times2 = []
    scale2 = []  # параметр обратный alpha
    for i in range(n):
        scale2.append(1 / random.random())

    for i in range(N):
        t_i = sys.maxsize  # время безотказной работы для i-ого эксперимента
        for i in range(n):
            new_value = numpy.random.exponential(scale2[i])
            # new_value = random.random() * 10
            if new_value < t_i:
                t_i = new_value
        times2.append(t_i)
    times2.sort()
    return times2

def model3(n, mode=1):
    times3 = []
    scale3 = []  # параметр обратный alpha
    for i in range(n):
        scale3.append(1 / random.random())

    if mode == 1:
        for i in range(N):
            t_i = 0  # время безотказной работы для i-ого эксперимента
            for i in range(n):
                new_value = numpy.random.exponential(scale3[i])
                if new_value > t_i:
                    t_i = new_value
            times3.append(t_i)
    else:
        for i in range(N):
            t_i = 0  # время безотказной работы для i-ого эксперимента
            for i in range(n):
                t_i += numpy.random.exponential(scale3[i])
            times3.append(t_i)
    times3.sort()
    return times3

N = 10000 # количество экспериментов (>= 150)
n = int(input('количество элементов системы (>= 1) = '))
k = int(input('количество подмножеств системы = '))
printGraph(model1(n, k), 'model1')
printGraph(model2(n), 'model2')
printGraph(model3(n, mode=1), 'model3.1')
printGraph(model3(n, mode=2), 'model3.2')