import random

lineDivider = '|============================================================================|'


def getStr(tempStr):
    diff = len(lineDivider) - len(tempStr) - 1
    for i in range(diff):
        tempStr += ' '
    tempStr += '|'
    return tempStr


p = 0.1
n_messages = 1000
totalMessages = 0
for i in range(n_messages):
    while True:
        totalMessages += 1
        if random.random() > p:
            break

print(lineDivider)
print(getStr('|'))
print(getStr("|     Среднее количество попыток для 1 пункта (Теор): " + str(1 / (1 - p))))
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
print(getStr("|     Среднее количество попыток для 2 пункта (Теор): " + str((1 - p ** max_retry) / (1 - p))))
print(getStr("|     Среднее количество попыток для 2 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)

pChannel = 0.1
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
print(getStr("|     Среднее количество попыток для 3.1 пункта (Теор): " + str(1 / (1 - p - pChannel + p * pChannel))))
print(getStr("|     Среднее количество попыток для 3.1 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)

totalMessages = 0
max_retry = 2
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
print(getStr("|     Среднее количество попыток для 3.1 пункта (Теор): " + str(
    (1 - (p + pChannel - p * pChannel) ** max_retry) / (1 - p - pChannel + p * pChannel))))
print(getStr("|     Среднее количество попыток для 3.1 пункта (Практ): " + str(totalMessages / n_messages)))
print(getStr('|'))
print(lineDivider)

p = 0.2
wait_time = 20

n_messages = 1000

n_retries = []
totalTime = 0
for i in range(n_messages):
    retries = 0
    while True:
        totalTime += wait_time
        if random.random() > p:
            print('message #', i, ' - ', retries, ' in time: ', totalTime)
            break
        else:
            retries += 1

    n_retries.append(retries)

utilization = (n_messages) / (totalTime)

print(f"Коэффициент использования канала (Теор): {utilization}")
print(f"Коэффициент использования канала (Практ): {(1 - p) / (1 + wait_time)}")

print('=============================================================================')

lineDivider = '|----------------------------------|'


def getStr(tempStr):
    diff = len(lineDivider) - len(tempStr) - 1
    for i in range(diff):
        tempStr += ' '
    tempStr += '|'
    return tempStr


successMessages = []
totalTime = 0
while len(successMessages) != n_messages:
    totalTime += wait_time
    for i in range(wait_time):
        if random.random() > p and len(successMessages) < n_messages:
            successMessages.append(0)
            print(getStr('| message #' + str(len(successMessages))))
        else:
            print(getStr('| error #' + str(len(successMessages))))
            break
    print(lineDivider)

utilization = (n_messages) / (totalTime)

print(f"Коэффициент использования канала (Теор): {utilization}")
print(f"Коэффициент использования канала (Практ): {(1 - p) / (1 + wait_time * p)}")

