import math
import random
import matplotlib.pyplot as plt

class SystemElement:
    def __init__(self):
        self.status = True
        self.recovery_id = -1

def is_system_working(system, parallel_elements, parallel_elements2):
    for i, element in enumerate(system):
        if not element.status and i not in parallel_elements and i not in parallel_elements2:
            return False

    for elements in [parallel_elements, parallel_elements2]:
        if all(not system[i].status for i in elements):
            return False
    
    return True

N = 10000
k = 100
delta_t = 0.1
time_line = [0] * k

system_amount = 5
system_elements = [SystemElement() for _ in range(system_amount)]
parallel_elements = [0, 1, 2]
parallel_elements2 = [3, 4]

recovery_amount = 3
system_recoveries = [True] * recovery_amount

lambda_element = 0.8
mu = 0.9

average_time_array = [0]
average_time_recovery_array = [0]

for _ in range(N):
    for t in range(k):
        for sys_id, system_element in enumerate(system_elements):
            if system_element.status:
                if random.random() >= math.exp(-(lambda_element * t * delta_t)):
                    system_element.status = False
                    for r, recovery in enumerate(system_recoveries):
                        if recovery:
                            system_element.recovery_id = r
                            system_recoveries[r] = False
                            break
            else:
                if random.random() <= math.exp(-(mu * delta_t)) and system_element.recovery_id != -1:
                    system_element.status = True
                    system_recoveries[system_element.recovery_id] = True
                    system_element.recovery_id = -1
                elif system_element.recovery_id == -1:
                    for r, recovery in enumerate(system_recoveries):
                        if recovery:
                            system_element.recovery_id = r
                            system_recoveries[r] = False
                            break
        
        if is_system_working(system_elements, parallel_elements, parallel_elements2):
            if average_time_recovery_array[-1] != 0:
                average_time_recovery_array.append(0)
            average_time_array[-1] += delta_t
            time_line[t] += 1
        else:
            if average_time_array[-1] != 0:
                average_time_array.append(0)
            average_time_recovery_array[-1] += delta_t

average_time = sum(average_time_array) / len(average_time_array)
average_time_recovery = sum(average_time_recovery_array) / len(average_time_recovery_array)
f_t = average_time / (average_time + average_time_recovery)

k_2_2 = (1 - (1 - mu / (mu + lambda_element)) ** 2)
k_3_3 = (1 - (1 - mu / (mu + lambda_element)) ** 3)
k_1_1 = mu / (mu + lambda_element)
k_2_1 = (2 * lambda_element * mu + mu ** 2) / (2 * (lambda_element ** 2) + 2 * lambda_element * mu + mu ** 2)
f_t_up = k_3_3 * k_2_2
f_t_lower = (1 - (1 - k_2_1) * (1 - k_1_1)) * k_2_1
f_t_lower_2 = k_2_2 * k_1_1

arguments = []
practical_values = []
theory_values = []
theory_values_upper = []
theory_values_lower = []
theory_values_lower_2 = []

for i in range(k):
    arguments.append(i * delta_t)
    practical_values.append(time_line[i] / N)
    theory_values.append(f_t)
    theory_values_upper.append(f_t_up)
    theory_values_lower.append(f_t_lower)
    theory_values_lower_2.append(f_t_lower_2)

plt.plot(arguments, practical_values, label='practical')
plt.plot(arguments, theory_values, label='theory')
plt.plot(arguments, theory_values_upper, label='theory upper')
plt.plot(arguments, theory_values_lower, label='theory lower 1')
plt.plot(arguments, theory_values_lower_2, label='theory lower 2')
plt.legend()
plt.title('Коэфф. готовности от времени')
plt.xlabel('t')
plt.ylabel('K(t)')
plt.show()