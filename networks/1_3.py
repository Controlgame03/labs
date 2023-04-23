import random

lineDivider = '|============================================================================|'


def f(p, po):
    return p + po - p * po

def getStr(tempStr):
    diff = len(lineDivider) - len(tempStr) - 1
    for i in range(diff):
        tempStr += ' '
    tempStr += '|'
    return tempStr

p = 0.1
n_messages = 10000
totalMessages = 0
for i in range(n_messages):
    while True:
        totalMessages += 1
        if random.random() > f(p, 0.9):
            break

print(lineDivider)
print(getStr('|'))
print(getStr("|     Среднее количество попыток для 1 пункта (Теор): " + str(1/(1-f(p,0.9)))))
print(getStr("|     Среднее количество попыток для 1 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)

totalMessages = 0
max_retry = 2
for i in range(n_messages):
    curRetries = 0
    while True:
        totalMessages += 1
        curRetries += 1
        if random.random() > p or curRetries >= max_retry:
            break

print(lineDivider)
print(getStr('|'))
print(getStr("|     Среднее количество попыток для 2 пункта (Теор): " + str((1 - p**max_retry)/(1-p))))
print(getStr("|     Среднее количество попыток для 2 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)


pChannel = 0.9
totalMessages = 0
for i in range(n_messages):
    while True:
        totalMessages += 1
        if random.random() <= p:
            continue
        if random.random() > pChannel:
            break
            
print(lineDivider)
print(getStr('|'))
print(getStr("|     Среднее количество попыток для 3.1 пункта (Теор): " + str(1/(1-f(p,pChannel)))))
print(getStr("|     Среднее количество попыток для 3.1 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)


totalMessages = 0
max_retry = 10
for i in range(n_messages):
    curRetries = 0
    while True:
        totalMessages += 1
        curRetries += 1
        if random.random() <= p:
            continue
        if random.random() > pChannel or curRetries >= max_retry:
            break
print(lineDivider)
print(getStr('|'))
print(getStr("|     Среднее количество попыток для 3.1 пункта (Теор): " + str((1 - (p + pChannel - p*pChannel) ** max_retry) / (1-p - pChannel + p * pChannel))))
print(getStr("|     Среднее количество попыток для 3.1 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)