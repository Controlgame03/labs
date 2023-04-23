import math
import random
import matplotlib.pyplot as plt

def isSystemWorking(system):
    count_parallel = 0
    for i in parallel_elements:
        if system[i].status == False:
            count_parallel += 1
    if count_parallel != 0 and count_parallel == len(parallel_elements):
        return False
    
    for i in range(len(system)):
        if system[i].status == False and i not in parallel_elements:
            return False
    return True

class SystemElement:
    status = True
    recovery_id = -1

N = 50000
k = 100
delta_t = 0.1
time_line = []

system_amount = 2
system_elements = []
for i in range(system_amount):
    system_elements.append(SystemElement())
parallel_elements = [0,1]

recovery_amount = 1
system_recoveries = []

for i in range(recovery_amount):
    system_recoveries.append(True)
lambda_element = 0.8
mu = 0.9

average_time_array = [0]
average_time_recovery_array = [0]

for i in range(k):
    time_line.append(0)

for i in range(N):
    for t in range(k):
        for sys_id in range(len(system_elements)):
            if (system_elements[sys_id].status):
                if random.random() >= math.exp(-(lambda_element * t * delta_t)):
                    system_elements[sys_id].status = False
                    for r in range(len(system_recoveries)):
                        if (system_recoveries[r]):
                            system_elements[sys_id].recovery_id =  r
                            system_recoveries[r] = False
                            break
            else:
                if random.random() <= math.exp(-(mu * delta_t)) and system_elements[sys_id].recovery_id != -1:
                    system_elements[sys_id].status = True
                    system_recoveries[system_elements[sys_id].recovery_id] = True
                    system_elements[sys_id].recovery_id = -1
                elif system_elements[sys_id].recovery_id == -1:
                    for r in range(len(system_recoveries)):
                        if (system_recoveries[r]):
                            system_elements[sys_id].recovery_id =  r
                            system_recoveries[r] = False
                            break
        
        if (isSystemWorking(system_elements)):
            if (average_time_recovery_array[-1] != 0):
                average_time_recovery_array.append(0)
            average_time_array[-1] = average_time_array[-1] + delta_t
            time_line[t] += 1
        else:
            if (average_time_array[-1] != 0):
                    average_time_array.append(0)
            average_time_recovery_array[-1] = average_time_recovery_array[-1] + delta_t
    

average_time = sum(average_time_array) / len(average_time_array)
average_time_recovery = sum(average_time_recovery_array) / len(average_time_recovery_array)
f_t = average_time / (average_time + average_time_recovery)

arguments = []
practical_values = []
theory_values = []
for i in range(k):
    arguments.append(i * delta_t)
    practical_values.append(time_line[i] / N)
    theory_values.append(f_t)

plt.plot(arguments, practical_values, label='practical')
plt.plot(arguments, theory_values, label='theory')
plt.legend()
plt.title('Коэфф. готовности от времени')
plt.xlabel('t')
plt.ylabel('K(t)')
plt.show()