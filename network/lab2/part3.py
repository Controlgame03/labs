import random
print("part 2.3.1")
#5 dfhbfyn
p = 0.1
n_messages = 10000
pBack = 0.99
totalMessages = 0
for i in range(n_messages):
    while True:
        totalMessages += 1
        if random.random() <= p:
            continue
        if random.random() > pBack:
            break

print("theoretical --> " + str(1 / (1 - p - pBack + p * pBack)))
print("practical --> " + str(totalMessages / n_messages))

print("\npart 2.3.2")
totalMessages = 0
max_retry = 2

for i in range(n_messages):
    curRetries = 0
    while True:
        curRetries += 1
        totalMessages += 1

        if random.random() > pBack or curRetries >= max_retry:
            break
        if random.random() <= p:
            continue


print("theoretical --> " + str((1 - (p + pBack - p * pBack) ** max_retry) / (1 - p - pBack + p * pBack)))
print("practical -->" + str(totalMessages / n_messages))
print(totalMessages)
print(n_messages)