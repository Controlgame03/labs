import random
import math
import numpy as np
class System:
    system_lambda = 0
    system_mu = 0
    delta_t = 0
    recovery_time = 1
    is_working = True
    def __init__(self, system_lambda, system_mu, delta_t):
        self.system_lambda = system_lambda
        self.system_mu = system_mu
        self.delta_t = delta_t
    def current_work_cycle(self, current_time, number_of_recovery_teams):
        if self.is_working:
            if random.random() < math.exp(-self.system_lambda * current_time):
                self.is_working = True
            else:
                self.is_working = False
        else:
            if random.random() > math.exp(-self.system_mu * self.recovery_time * delta_t) and number_of_recovery_teams != 0:
                self.is_working = True
                self.recovery_time = 1
            else:
                self.is_working = False
                self.recovery_time += 1
        return self.is_working

number_of_experiments= 10000
working_step = 300
delta_t = 0.01
recovery_teams = 100000000000

systems = []
systems.append(System(system_lambda=0.7, system_mu=0.3, delta_t=delta_t))
systems.append(System(system_lambda=0.6, system_mu=0.2, delta_t=delta_t))

result_time_line = []
for i in range(working_step):
    result_time_line.append(0)

for current_experiment in range(number_of_experiments):
    for current_step in range(working_step):
        for system in systems:
            if not(system.current_work_cycle(current_time=current_step*delta_t, number_of_recovery_teams=recovery_teams)) and recovery_teams != 0:
                recovery_teams -= 1

        #можно задать интерестующую схему из len(systems) элементов. В данном примере: параллельно соединенные два элемента
        if systems[0].is_working or systems[1].is_working:
            result_time_line[current_step] += 1
print(result_time_line)
