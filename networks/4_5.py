import random

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
            print('message #', i, ' - ', retries,  ' in time: ', totalTime)
            break
        else:
            retries += 1
            
    n_retries.append(retries)

utilization = (n_messages)/ (totalTime)

print(f"Коэффициент использования канала (Теор): {utilization}")
print(f"Коэффициент использования канала (Практ): {(1 - p)/(1 + wait_time)}")

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

utilization = (n_messages)/ (totalTime)

print(f"Коэффициент использования канала (Теор): {utilization}")
print(f"Коэффициент использования канала (Практ): {(1 - p)/(1 + wait_time * p)}")