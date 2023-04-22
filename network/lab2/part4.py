import random

p = 0.2
wait_time = 3

n_messages = 10

n_retries = []
totalTime = 0
for i in range(n_messages):
    retries = 0
    while True:
        totalTime += wait_time
        totalTime += 1
        if random.random() > p:
            print('message №', i, ' received in ', retries + 1, 'attempts. in time: ', totalTime)
            break
        else:
            retries += 1

    n_retries.append(retries)

utilization = (n_messages) / (totalTime)

print("theoretical --> " + str(utilization))
print("practical -- > " +  str((1 - p) / (1 + wait_time)))