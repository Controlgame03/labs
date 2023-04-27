import matplotlib.pyplot as plt
import random
import numpy as np

n_messages = 800
max_size = 3

def getN(p, wait_time):
    successMessages = []
    virtual_channels = []

    for i in range(wait_time + 1):
        virtual_channels.append([])

    next_value = 0
    next_values = [i for i in range(wait_time + 1)]
    max_next = 0
    
    timeTotal = 0

    c = 0
    while len(successMessages) < n_messages:
        timeTotal += wait_time + 1
        for i in range(wait_time + 1):
            max_next = max(max_next, np.max(next_values))
            message = next_values.pop(0)
            
            temp_p = random.random()
            if message < n_messages:
                c += 1
                
            if temp_p > p and message < n_messages and len(virtual_channels[i]) < max_size:
                virtual_channels[i].append(message)
                
                next_values.append(max_next + 1)
            else:
                next_values.append(message)
            
            if len(virtual_channels[i]) != 0 and virtual_channels[i][0] == next_value:
                successMessages.append(virtual_channels[i].pop(0))
                next_value += 1

    return c / n_messages, n_messages / timeTotal

# point # 4 a
arguments = [i / 10 for i in range(10)] # p
t_array = [2, 4, 5, 7]
for t in t_array:
    values = []
    for i in arguments:
        temp_average, temp_t = getN(i, t)
        values.append(temp_t)
    plt.plot(arguments, values, label='t = ' + str(t))
plt.legend()
plt.title('Коэффициента использования канала \n от вероятности ошибки в канале')
plt.xlabel('Вероятность')
plt.ylabel('Коэффициента использования канала')
plt.show()

# point # 4 b
arguments = [i for i in range(20)]
p_array = [0.3, 0.5, 0.7, 0.9]
for p in p_array:
    values = []
    for i in arguments:
        temp_average, temp_t = getN(p, t)
        values.append(temp_t)

    plt.plot(arguments, values, label='p = ' + str(p))
plt.legend()
plt.title('Коэффициента использования канала \n от задержки получения квитанции')
plt.xlabel('Задержка получения квитанции')
plt.ylabel('Коэффициента использования канала')
plt.show()

# point # 4 c
arguments = [i / 10 for i in range(10)] # p
t_array = [2, 4, 5, 7]
for t in t_array:
    values = []
    for i in arguments:
        temp_average, temp_t = getN(i, t)
        values.append(temp_average)
    plt.plot(arguments, values, label='t = ' + str(t))
plt.legend()
plt.title('Среднего числа повторных передач \n от вероятности ошибки в канале')
plt.xlabel('Вероятность')
plt.ylabel('Среднее числа повторных передач')
plt.show()

# point # 4 d
arguments = [i for i in range(20)]
p_array = [0.3, 0.5, 0.7, 0.9]
for p in p_array:
    values = []
    for i in arguments:
        temp_average, temp_t = getN(p, t)
        values.append(temp_average)

    plt.plot(arguments, values, label='p = ' + str(p))
plt.legend()
plt.title('Среднего числа повторных передач \n от величины задержки получения квитанции')
plt.xlabel('Задержка получения квитанции')
plt.ylabel('Среднее числа повторных передач')
plt.show()