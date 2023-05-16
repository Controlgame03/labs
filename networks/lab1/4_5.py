import random
import matplotlib.pyplot as plt

p = 0.5
wait_time = 2

n_messages = 100

n_retries = []
totalTime = 0
for i in range(n_messages):
    retries = 0
    while True:
        totalTime += wait_time + 1
        if random.random() > p:
           # print('сообщение #', i, ' - ', retries,  ' время: ', totalTime)
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
    return tempStr

successMessages = []
totalTime = 0

while len(successMessages) != n_messages:
     
    for i in range(wait_time):
        if random.random() > p and len(successMessages) < n_messages:
            successMessages.append(0)
            print(getStr('сообщение №' + str(len(successMessages)) + ', время = ' + str(totalTime + i)))
        else:
            
            print(getStr('ошибка №' + str(len(successMessages) + 1) + ', время = ' + str(totalTime + i) ))
            totalTime += 1
            break
    totalTime += wait_time

utilization = (n_messages)/ (totalTime)

print(f"Коэффициент использования канала (Практ): {utilization}")
print(f"Коэффициент использования канала (Теор): {(1 - p)/(1 + wait_time * p)}")