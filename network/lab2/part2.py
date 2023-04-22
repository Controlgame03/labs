import random

p = 0.1
n_messages = 100000
totalMessages = 0
max_retry = 4
for i in range(n_messages):
    curRetries = 0
    while True:
        totalMessages += 1
        curRetries += 1
        if random.random() > p or curRetries >= max_retry:
            break
print("part 2.2.")
print("theoretical --> " + str((1 - p**max_retry)/(1-p)))
print("practical --> " + str(totalMessages / n_messages))