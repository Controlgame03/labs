import random
import math
import numpy as np
import matplotlib.pyplot as plt

# что еще нужно сделать:
# 1/ наладить синхронизацию по recovery_teams
# 2/ вычислять теоретический коэф. готовности
#       2.1/ вычислять инетрвалы T и T(восстан)

class System:
    def __init__(self, system_lambda, system_mu, delta_t):
        self.system_lambda = system_lambda
        self.system_mu = system_mu
        self.delta_t = delta_t
        self.is_working = True
        self.recovery_time = 0

        global recovery_teams
        recovery_teams = 1000000

        self.ready_to_recovery = False
    def current_work_cycle(self, current_time):
        global recovery_teams
        if self.is_working:
            if random.random() < math.exp(-self.system_lambda * current_time):
                self.is_working = True
            else:
                self.is_working = False
        else:
            if not(self.ready_to_recovery) and recovery_teams <= 0:
                return self.is_working
            if not(self.ready_to_recovery):
                recovery_teams -= 1
                self.ready_to_recovery = True
            if random.random() > math.exp(-self.system_mu * self.recovery_time * delta_t):
                self.is_working = True
                self.recovery_time = 1
                recovery_teams += 1
            else:
                self.is_working = False
                self.recovery_time += 1
        return self.is_working

number_of_experiments= 100
working_step = 300
delta_t = 0.01

systems = []
systems.append(System(system_lambda=0.7, system_mu=1.7, delta_t=delta_t))
systems.append(System(system_lambda=1.6, system_mu=1.7, delta_t=delta_t))
systems.append(System(system_lambda=1.7, system_mu=1.8, delta_t=delta_t))
systems.append(System(system_lambda=1.6, system_mu=1.8, delta_t=delta_t))
systems.append(System(system_lambda=1.7, system_mu=1.7, delta_t=delta_t))
systems.append(System(system_lambda=1.6, system_mu=1.8, delta_t=delta_t))

result_time_line = []
for i in range(working_step):
    result_time_line.append(0)

for current_experiment in range(number_of_experiments):
    for current_step in range(working_step):
        for system in systems:
            system.current_work_cycle(current_time=current_step * delta_t)

        #можно задать интерестующую схему из len(systems) элементов. В данном примере: параллельно соединенные два элемента
        if systems[0].is_working or systems[1].is_working or systems[2].is_working or systems[3].is_working or systems[4].is_working or systems[5].is_working:
            result_time_line[current_step] += 1
    for system in systems:
        system.is_working = True

#print(result_time_line)

arguments = []
practical_values = []
for current_step in range(working_step):
    arguments.append(current_step * delta_t)
    practical_values.append(result_time_line[current_step] / number_of_experiments)

print(sum(practical_values))

plt.plot(arguments, practical_values, label='practical')
#plt.plot(arguments, theory_values, label='theory')
plt.legend()
plt.title('Зависимость коэфф. готовности от времени')
plt.xlabel('t')
plt.ylabel('K(t)')
plt.show()