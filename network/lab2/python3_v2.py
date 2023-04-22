import random

p = 0.2
wait_time = 2
n_messages = 10
totalTime = 0

successMessages = []
totalTime = 0
while len(successMessages) != n_messages:
    totalTime += wait_time
    for i in range(wait_time):
        if random.random() > p and len(successMessages) < n_messages:
            successMessages.append(0)
            print('message #' + str(len(successMessages)))
        else:
            print('error #' + str(len(successMessages)))
            break

utilization = (n_messages)/ (totalTime)

print(f"Коэффициент использования канала (Теор): {utilization}")
print(f"Коэффициент использования канала (Практ): {(1 - p)/(1 + wait_time * p)}")