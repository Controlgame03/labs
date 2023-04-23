import random
import matplotlib.pyplot as plt

p = 0.4
wait_time = 2

n_messages = 10000

n_retries = []
totalTime = 0
for i in range(n_messages):
    retries = 0
    while True:
        totalTime += wait_time + 1
        if random.random() > p:
            # print('message #', i, ' - ', retries,  ' in time: ', totalTime)
            break
        else:
            retries += 1
            
    n_retries.append(retries)

utilization = (n_messages)/ (totalTime)

print(f"Коэффициент использования канала (Практ): {utilization}")
print(f"Коэффициент использования канала (Теор): {(1 - p)/(1 + wait_time)}")

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
allT = {}

while len(successMessages) != n_messages:
    totalTime += wait_time 
    for i in range(wait_time):
        if random.random() > p and len(successMessages) < n_messages:
            successMessages.append(0)
            # print(getStr('| message #' + str(len(successMessages)) + ' at time = ' + str(totalTime)))
        else:
            id = len(successMessages)
            allT[id] = 1 if id not in allT else allT[id] + 1
            totalTime += 1
            # print(getStr('| error #' + str(len(successMessages)) + ' at time = ' + str(totalTime) ))
            break
    
    # print(lineDivider)

utilization = (n_messages)/ (totalTime)

print(f"Коэффициент использования канала (Практ): {utilization}")
print(f"Коэффициент использования канала (Теор): {(1 - p)/(1 + wait_time * p)}")


plt.plot(allT.keys(), allT.values())
plt.title('Количество ошибок от номера сообщения')
plt.xlabel('сообщение')
plt.ylabel('ошибки')
plt.show()