import random
import sys
import numpy.random
import matplotlib.pyplot as plt

##########имитационное моделирование##########
def experiment_i():
    t_i = sys.maxsize # время безотказной работы для i-ого эксперимента

    for i in range(n):
        new_value = numpy.random.exponential(scale[i])
        #new_value = random.random() * 10
        if new_value < t_i:
            t_i = new_value
    return t_i

N = 10000 # количество экспериментов (>= 150)

t = [] # массив времён безотказной работы

n = int(input('количество элементов системы (>= 1) = '))

alpha = [] # характеристики элементов
koef = 10
for i in range(n):
    alpha.append(koef * random.random())

scale = []  # параметр обратный alpha
for i in range(n):
    scale.append(1 / alpha[i])



for i in range(N):
    t.append(experiment_i())

t.sort()

print("min_t = ", t[0])
print("max_t = ", t[len(t) - 1])
##############################################

##############построение графика##############
def workable_systems(arr, time, delta=0):
    count = 0
    for i in range(len(arr)):
        if arr[i] > time + delta:
            count += 1
    return count

################
#справочные значения (стр.8)
number_of_points = 60
tm = t[len(t) - 110]
t_step = tm / number_of_points
delta_t = 0.1 * t_step
#################

arguments = []
values = []
lower_limit = t[0]
upper_limit = tm

print("lower_limit=", lower_limit)
print("upper_limit= ", upper_limit)

for i in range(1, number_of_points):
    arguments.append(lower_limit + i * (upper_limit - lower_limit) / number_of_points)

for i in range(len(arguments)):
    n_t = workable_systems(t, arguments[i])
    n_t_delta = workable_systems(t, arguments[i], delta_t)
    values.append((n_t - n_t_delta)/(n_t * delta_t))


print("Tm= ", tm)
print("t_step= ", t_step)
print("delta_t= ", delta_t)

# строим график
plt.plot(arguments, values)

# задаем заголовок графика
plt.title('Зависимость alpha(t) оценки интенсивности отказов от времени.')

# задаем название оси x
plt.xlabel('Значения t')

# задаем название оси y
plt.ylabel('Значения alpha(t)')

# выводим график на экран
plt.show()
##############################################