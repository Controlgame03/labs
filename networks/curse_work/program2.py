# lab03 networks

import random
import math
import matplotlib.pyplot as plt

window_quantity = 1000000 # максимальное количество окон
total_time = 10000 # время работы системы
input_lambda = 0.0 # начальная лямда
# probability = 0.5
M = 250 # количество пользователей
precision = 10 # точность построения графиков

success_delay = 1.0
conf_delay = 2.0
empt_delay = 0.5

p = 1 / M


def poisson_stream(input_lambda): # сколько сообщений появилось в новом окне
    messages_count = 0
    exp = math.exp(-input_lambda)
    random_int = random.random()
    while random_int > exp:
        messages_count += 1
        exp += math.exp(-input_lambda) * (input_lambda**messages_count) / math.factorial(messages_count)
    return messages_count

def message_will_be_sent_aloha():
    if random.random() > (1 - p):
        return True
    else:
        return False
    

def model(subscriber_quantity, input_lambda, conflict_delay, empty_delay):
    
    subscribers_delay = [] # хранятся сообщения, которые в очереди 
    send_messages = [] # хранятся задержки отправленных сообщений
    message_amount = []
    total_delay = 0
    for _ in range(subscriber_quantity):
        subscribers_delay.append([])
        send_messages.append([])
    
    wishing_send_amount = [] # хранится количество пользователей, захотевших отправить сообщение в текущем окне


    for current_window in range(window_quantity):
        if total_delay > total_time:
            # print(total_delay) 
            # print(current_window)
            break
        current_queue = [] # номера пользователей, захотевших отправить сообщение

        message_amount.append(0)
        for i in subscribers_delay:
            message_amount[-1] += len(i)

        for subscriber in range(subscriber_quantity):
            if len(subscribers_delay[subscriber]) != 0 and message_will_be_sent_aloha():
                current_queue.append(subscriber)
        wishing_send_amount.append(len(current_queue))
        
        delay = 0

        if wishing_send_amount[-1] == 0: # пусто
            delay = empty_delay
            pass
        elif wishing_send_amount[-1] == 1: # успех
            delay = success_delay
            messager_number = current_queue[0]
            send_messages[messager_number].append(subscribers_delay[messager_number][0])
            subscribers_delay[messager_number].pop(0)
        else: # конфликт
            delay = conflict_delay
        
        total_delay += delay
        messages_count = 0
        if delay != 0:
            messages_count = poisson_stream(input_lambda*delay)
        
        for _ in range(messages_count):
            subscriber_number = random.SystemRandom().randint(0, subscriber_quantity - 1)
            subscribers_delay[subscriber_number].append(0)
        
        for subscriber in subscribers_delay:
            for message in range(len(subscriber)):
                subscriber[message] += delay
    
    average_delay = 0 # сумма всех чисел из send_messages поделенная на len(send_mes)
    output_mu = 0 # len(send_mes)/количество окон
    for i in range(len(send_messages)):
        average_delay += sum(send_messages[i])
        output_mu += len(send_messages[i])
    if output_mu == 0:
        average_delay = 0
    else:
        average_delay = average_delay / output_mu
    output_mu = output_mu / total_delay
        
    # average_subscribers = 0 # среднее из wishing_send_amount
    # average_subscribers = sum(wishing_send_amount) / len(wishing_send_amount)

    average_message_amount = sum(message_amount) / len(message_amount)
    
    return [average_delay, average_message_amount, output_mu, total_delay]
    # return [average_delay, average_subscribers, output_mu]

average_delays = []
average_subscribers = []
output_mus = []
arguments = []
total_delays = []

for _ in range(int(1.0 * precision)):
    result = model(M, input_lambda, conf_delay, empt_delay)
    average_delays.append(result[0])
    average_subscribers.append(result[1])
    output_mus.append(result[2])
    total_delays.append(result[3])
    arguments.append(input_lambda)
    input_lambda += 1 / precision
print("lambda = " + str(input_lambda))
print("average_delays = " + str(average_delays))
print("average_subscribers = " + str(average_subscribers))
print("output_mus = " + str(output_mus))

average_delays_basic = []
average_subscribers_basic = []
output_mus_basic = []
total_delays_basic = []
input_lambda = 0
e_m = 1/2.7182818284
lambda_crit_aloha = (e_m)/(e_m*success_delay + e_m * empt_delay + (1-2*e_m)*conf_delay)
crit = []
for _ in range(len(arguments)):
    crit.append(lambda_crit_aloha)



plt.plot(arguments, average_delays, label='УДЭО')
# plt.plot(arguments, average_delays_basic, label='ДЭО')
plt.axvline(x=lambda_crit_aloha)
plt.legend()
plt.title('Средняя задержка. ')
plt.xlabel('lambda')
plt.ylabel('d(lambda)')
plt.show()


plt.plot(arguments, average_subscribers, label='УДЭО')
# plt.plot(arguments, average_subscribers_basic, label='ДЭО')
plt.axvline(x=lambda_crit_aloha)
plt.legend()
plt.title('Среднее количество сообщений. ')
plt.xlabel('lambda')
plt.ylabel('N')
plt.show()

plt.plot(arguments, output_mus, label='УДЭО')
# plt.plot(arguments, output_mus_basic, label='ДЭО')
plt.plot(arguments, crit)
plt.legend()
plt.title('Интенсивность выходного потока. ')
plt.xlabel('lambda')
plt.ylabel('mu')
plt.show()

# plt.plot(arguments, total_delays, label='УДЭО')
# plt.plot(arguments, total_delays_basic, label='ДЭО')
# plt.legend()
# plt.title('Общее время работы канала. ' + info)
# plt.xlabel('lambda')
# plt.ylabel('time')
# plt.show()
