import random
import numpy as np

p = 0.5
wait_time = 15

n_messages = 800

successMessages = []
virtual_channels = []

for i in range(wait_time + 1):
    virtual_channels.append([])

next_value = 0
next_values = [i for i in range(wait_time + 1)]
max_next = 0
while len(successMessages) < n_messages:
    
    for i in range(wait_time + 1):
        max_next = max(max_next, np.max(next_values))
        message = next_values.pop(0)
        temp_p = random.random()
        
        if temp_p > p and message < n_messages:
           virtual_channels[i].append(message)
           
           next_values.append(max_next + 1)
        else:
            next_values.append(message)
        
        if len(virtual_channels[i]) != 0 and virtual_channels[i][0] == next_value:
            successMessages.append(virtual_channels[i].pop(0))
            next_value += 1
        print(virtual_channels[i])
    print('-----------------')

print(successMessages[-1])