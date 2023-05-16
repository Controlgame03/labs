import matplotlib.pyplot as plt
import random
import numpy as np

p = 0.4
wait_time = 2

n_messages = 1000

def model_with_logs(p, wait_time):
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

        for i in range(wait_time + 1):
            max_next = max(max_next, np.max(next_values))
            message = next_values.pop(0)

            temp_p = random.random()
            if message < n_messages:
                c += 1
            status = ' успешно '
            if temp_p > p and message <= n_messages:
               virtual_channels[i].append(message)
               next_values.append(max_next + 1)
            else:
                status = ' ошибка '
                next_values.append(message)
            logStr = str(timeTotal + i) + ') канал №' + str(i) + ', буффер: ' + str(virtual_channels[i]) + ', сообщение №' + str(message) + ' =' + status

            if len(virtual_channels[i]) != 0 and virtual_channels[i][0] == next_value:
                successMessages.append(virtual_channels[i].pop(0))
                logStr += '   |   '+ str(next_value) + ' ---> '
                next_value += 1
            print(logStr)
        timeTotal += wait_time + 1
    return c / n_messages, n_messages / timeTotal

temp_average, utilization = model_with_logs(p, wait_time)

print(f"Коэффициент использования канала (Практ): {utilization}")
print(f"Коэффициент использования канала (Теор): {(1 - p)}")
print(f"Среднее количество сообщений: {temp_average}")


def model_without_logs(p, wait_time):
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

            if temp_p > p and message < n_messages:
                virtual_channels[i].append(message)

                next_values.append(max_next + 1)
            else:
                next_values.append(message)

            if len(virtual_channels[i]) != 0 and virtual_channels[i][0] == next_value:
                successMessages.append(virtual_channels[i].pop(0))
                next_value += 1

    return c / n_messages, n_messages / timeTotal

# 5a
arguments = [i / 10 for i in range(10)] # p
t_array = [2, 4, 5, 7]
for t in t_array:
    values = []
    for i in arguments:
        temp_average, temp_t = model_without_logs(i, t)
        values.append(temp_t)
    plt.plot(arguments, values, label='t = ' + str(t))
plt.legend()
plt.title('Практика. Алг. с вирт. каналами. Зав-сть коэффициента \n использования канала от вероятности ошибки в канале')
plt.xlabel('Вероятность ошибки в канале')
plt.ylabel('Коэффициента использования канала')
plt.show()

#5b
arguments = [i for i in range(20)]
p_array = [0.3, 0.5, 0.7, 0.9]
for p in p_array:
    values = []
    for i in arguments:
        temp_average, temp_t = model_without_logs(p, t)
        values.append(temp_t)

    plt.plot(arguments, values, label='p = ' + str(p))
plt.legend()
plt.title('Практика. Алг. с вирт. каналами. Зав-сть коэффициента \n  использования канала от задержки получения квитанции')
plt.xlabel('Задержка получения квитанции')
plt.ylabel('Коэффициента использования канала')
plt.show()

#5c
arguments = [i / 10 for i in range(10)] # p
t_array = [2, 4, 5, 7]
for t in t_array:
    values = []
    for i in arguments:
        temp_average, temp_t = model_without_logs(i, t)
        values.append(temp_average)
    plt.plot(arguments, values, label='t = ' + str(t))
plt.legend()
plt.title('Практика. Алг. с вирт. каналами. Зав-сть среднего числа \n повторных передач от вероятности ошибки в канале')
plt.xlabel('Вероятность ошибки в канале')
plt.ylabel('Среднее числа повторных передач')
plt.show()

#5d
arguments = [i for i in range(20)]
p_array = [0.3, 0.5, 0.7, 0.9]
for p in p_array:
    values = []
    for i in arguments:
        temp_average, temp_t = model_without_logs(p, t)
        values.append(temp_average)
    plt.plot(arguments, values, label='p = ' + str(p))
plt.legend()
plt.title('Практика. Алг. с вирт. каналами. Зав-сть среднего числа \n повторных передач от величины задержки получения квитанции')
plt.xlabel('Задержка получения квитанции')
plt.ylabel('Среднее числа повторных передач')
plt.show()

#6.1
arguments = [i / 10 for i in range(11)] # p
t_array = [2, 4, 5, 7]
for t in t_array:
    values = []
    for i in arguments:
        temp = (1 - i) / (1 + i * t)
        values.append(temp)

    plt.plot(arguments, values, label='t = ' + str(t))
plt.legend()
plt.title('Теория. Алг. с возвратом.  Зав-сть коэффициента \n использования канала от вероятности ошибки в прямом канале')
plt.xlabel('Вероятность')
plt.ylabel('Коэффициент использования канала')
plt.show()

#6.2
arguments = [i for i in range(20)]
p_array = [0.3, 0.5, 0.7, 0.9]
for p in p_array:
    values = []
    for i in arguments:
        temp = (1 - p) / (1 + p * i)
        values.append(temp)

    plt.plot(arguments, values, label='p = ' + str(p))
plt.legend()
plt.title('Теория. Алг. с возвратом.  Зав-сть коэффициента \n использования канала от величины задержки получения квитанции')
plt.xlabel('Задержка получения квитанции')
plt.ylabel('Коэффициент использования канала')
plt.show()