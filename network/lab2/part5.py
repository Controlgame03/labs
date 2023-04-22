import random

p = 0.2
wait_time = 2
n_messages = 10
totalTime = 0

successMessages = []
totalTime = 0
logResiever = []
logSender = []

for i in range(10 * n_messages):
    logResiever.append("")
    logSender.append("")
i = 1

while len(successMessages) != n_messages:
    totalTime += 1
    logSender.append(i)
    if random.random() > p and len(successMessages) < n_messages:
        logResiever.insert(totalTime + wait_time, 1)
        successMessages.append(0)
        print('message №' + str(len(successMessages)) + " successfully received")
        i += 1
    else:
        logResiever.insert(totalTime + wait_time, 1)
        logResiever.append(0)
        print('message №' + str(len(successMessages)) + " received with an error")

utilization = (n_messages) / (totalTime)

print("theoretical --> " + str(utilization))
print("practical --> " + str((1 - p) / (1 + wait_time * p)))
print(totalTime)
