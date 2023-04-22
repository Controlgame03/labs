import random

p = 0.1
n_messages = 100000
totalMessages = 0
for i in range(n_messages):
    while True:
        totalMessages += 1
        if random.random() > p:
            break
print("part 2.1.")
print("theoretical --> " + str(1/(1-p)))
print("practical --> " + str(totalMessages / n_messages))
