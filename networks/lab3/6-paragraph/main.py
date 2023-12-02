import random
import math
import matplotlib.pyplot as plt

def generate_poisson(lam):
    x = 0
    p = math.exp(-lam)
    u = random.random()
    while u > p:
        x += 1
        p += math.exp(-lam) * (lam**x) / math.factorial(x)
    return x


requestAmount = 100000
curLambda = 0.1

arguments = []
values = []

averageMessages = []

for _ in range(9):
    store = []
    messages = []
    valuesMessages = []
    for i in range(requestAmount):
        for id in range(len(messages)):
            messages[id] = messages[id] + 1
        
        if (len(messages) > 0):
            temp = messages.pop(0)
            store.append(temp)

        sendersAmount = generate_poisson(curLambda)

        # tempMes = [random.random() for _ in range(sendersAmount)] #sync
        tempMes = [0 for _ in range(sendersAmount)] #async

        messages = messages + tempMes
        valuesMessages.append(len(messages))

    total = 0
    for s in store:
        total = total + s

    arguments.append(curLambda)
    totalMes = 0
    for i in valuesMessages:
        totalMes = totalMes + i
    
    averageMessages.append(totalMes / len(valuesMessages))
    values.append((total) / len(store))
    curLambda = curLambda + 0.1


valuesTheory= []
for p in arguments:
    #n = ( (2 - p)) / (2 * (1 - p)) + 0.5 #sync
    n = ( (2 - p)) / (2 * (1 - p)) #async
    valuesTheory.append(n)
    
plt.plot(arguments, values, label='Синхронная (практ)')
plt.plot(arguments, valuesTheory, label='Синхронная (теор)')
plt.legend()
plt.title('Средняя задержка')
plt.xlabel('lambda')
plt.ylabel('d(lambda)')
plt.show()

valuesTheory= []
for p in arguments:
    n = ( (2 - p) * p) / (2 * (1 - p))
    valuesTheory.append(n)
plt.plot(arguments, averageMessages, label='практ')
plt.plot(arguments, valuesTheory, label='теор')
plt.legend()
plt.title('Среднее количество пользователей')
plt.xlabel('lambda')
plt.ylabel('N')
plt.show()