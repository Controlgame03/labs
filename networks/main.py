import matplotlib.pyplot as plt
import random
import numpy as np

p = 0.9
wait_time = 15

n_messages = 800

successMessages = []
virtual_channels = []

max_size = 3

for i in range(wait_time + 1):
    virtual_channels.append([])

next_value = 0
next_values = [i for i in range(wait_time + 1)]
max_next = 0

totalTime = 0

c = 0
while len(successMessages) < n_messages:
    totalTime += wait_time + 1
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
        # print(virtual_channels[i])
    print(next_values)
    print('-----------------')

print(successMessages[-1])
print(totalTime)
utilization = (c)/ (totalTime)

print(f"Коэффициент использования канала (Практ): {utilization}")
print(f"Коэффициент использования канала (Теор): {(1 - (p * max_size) / (wait_time + 1))}")


print(f"Среднее количество сообщений: {(c / n_messages)}")



# point #6
arguments = [i / 10 for i in range(11)] # p
t_array = [2, 4, 5, 7]
for t in t_array:
    values = []
    for i in arguments:
        temp = (1 - i) / (1 + i * t)
        values.append(temp)

    plt.plot(arguments, values, label='t = ' + str(t))
plt.legend()
plt.title('Коэффициента использования канала \n от вероятности ошибки в прямом канале')
plt.xlabel('Вероятность')
plt.ylabel('Коэффициент использования канала')
plt.show()

arguments = [i for i in range(20)]
p_array = [0.3, 0.5, 0.7, 0.9]
for p in p_array:
    values = []
    for i in arguments:
        temp = (1 - p) / (1 + p * i)
        values.append(temp)

    plt.plot(arguments, values, label='p = ' + str(p))
plt.legend()
plt.title('Коэффициента использования канала \n от величины задержки получения квитанции')
plt.xlabel('Задержка получения квитанции')
plt.ylabel('Коэффициент использования канала')
plt.show()