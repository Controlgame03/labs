import math
import numpy.random
import matplotlib.pyplot as plt

N = 50000
k = 100
delta_t = 0.1
time_line = []
system_element = True
lambda_element = 0.8
mu = 0.9

# Не факт что эти значения нужны т к использую только для того,
# чтобы в цикле определять в какое состояние перехрдит система
o_to_o_probability = math.exp(-mu) # из 0 в 0
s1_to_s1_probability = math.exp(-lambda_element) #  из 1 в 1

average_time_array = [0]
average_time_recovery_array = [0]

for i in range(k):
    time_line.append(0)

for i in range(N):
    for t in range(k):
        if (system_element):
            p = numpy.random.exponential(1/lambda_element)
            if s1_to_s1_probability > p:
                average_time_array[-1] = average_time_array[-1] + delta_t
                time_line[t] += 1
            else:
                if (average_time_recovery_array[-1] != 0):
                    average_time_recovery_array.append(0)
                system_element = False
        else:
            p = numpy.random.exponential(1/mu)
            if o_to_o_probability <= p:
                if (average_time_array[-1] != 0):
                    average_time_array.append(0)
                system_element = True
                time_line[t] += 1
            else:
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