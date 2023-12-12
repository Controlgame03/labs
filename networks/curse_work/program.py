# lab03 networks

import random
import math
import matplotlib.pyplot as plt

window_quantity = 10000 # количество окон
input_lambda = 0.0 # не менять. начальная лямда
# probability = 0.5
M = 2 # количество пользователей
w_min = 2 # минимальная ширина окна
w_max = 128 #максимальная ширина окна
queue_size = None # можно поставить численное значение
precision = 10 # точность построения графиков

success_delay = 1
conf_delay = 0.3
empt_delay = 0.3


def poisson_stream(input_lambda): # сколько сообщений появилось в новом окне
    messages_count = 0
    exp = math.exp(-input_lambda)
    random_int = random.random()
    while random_int > exp:
        messages_count += 1
        exp += math.exp(-input_lambda) * (input_lambda**messages_count) / math.factorial(messages_count)
    return messages_count
    
def message_will_be_sent_interval(current_window, stats):
    if stats['window_number'] == current_window or stats['window_number'] == 0:
        return True 
    return False

def model(subscriber_quantity, input_lambda, queue_size, conflict_delay, empty_delay):
    if input_lambda == 0.8:
        pass
    subscribers_delay = [] # хранятся сообщения, которые в очереди 
    send_messages = [] # хранятся задержки отправленных сообщений
    subscriber_stats = [] # хранится ширина окна и номер выбранного окна абонента
    message_amount = []
    total_delay = 0
    for _ in range(subscriber_quantity):
        subscribers_delay.append([])
        send_messages.append([])
        subscriber_stats.append(dict(width=w_min, window_number=0))
    
    wishing_send_amount = [] # хранится количество пользователей, захотевших отправить сообщение в текущем окне

    for current_window in range(window_quantity):
        current_queue = [] # номера пользователей, захотевших отправить сообщение

        message_amount.append(0)
        for i in subscribers_delay:
            message_amount[-1] += len(i)

        for subscriber in range(subscriber_quantity):
            if len(subscribers_delay[subscriber]) != 0 and message_will_be_sent_interval(current_window, subscriber_stats[subscriber]):
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
            subscriber_stats[messager_number]['width'] = w_min
            if len(subscribers_delay[messager_number]) != 0:
                subscriber_stats[messager_number]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[messager_number]['width'])
        else: # конфликт
            delay = conflict_delay
            for subscriber in current_queue:
                subscriber_stats[subscriber]['width'] = min(subscriber_stats[subscriber]['width'] * 2, w_max)
                subscriber_stats[subscriber]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[subscriber]['width'])
        
        total_delay += delay
        messages_count = 0
        if delay != 0:
            messages_count = poisson_stream(input_lambda*delay)
        
        for _ in range(messages_count):
            subscriber_number = random.SystemRandom().randint(0, subscriber_quantity - 1)
            if queue_size == None or len(subscribers_delay[subscriber_number]) < queue_size:
                if len(subscribers_delay[subscriber_number]) == 0:
                    subscriber_stats[subscriber_number]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[subscriber]['width'])
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
    result = model(M, input_lambda, queue_size, conf_delay, empt_delay)
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

for _ in range(int(1.0 * precision)):
    result = model(M, input_lambda, queue_size, 1, 1)
    average_delays_basic.append(result[0])
    average_subscribers_basic.append(result[1])
    output_mus_basic.append(result[2])
    total_delays_basic.append(result[3])
    input_lambda += 1 / precision


info = "M=" + str(M) + ",QSIZE=" + str(queue_size) + " (W_MIN=" + str(w_min) + ",W_MAX=" + str(w_max) + ")"
plt.plot(arguments, average_delays, label='УДЭО')
plt.plot(arguments, average_delays_basic, label='ДЭО')
plt.legend()
plt.title('Средняя задержка. ' + info)
plt.xlabel('lambda')
plt.ylabel('d(lambda)')
plt.show()


plt.plot(arguments, average_subscribers, label='УДЭО')
plt.plot(arguments, average_subscribers_basic, label='ДЭО')
plt.legend()
plt.title('Среднее количество сообщений. ' + info)
plt.xlabel('lambda')
plt.ylabel('N')
plt.show()

plt.plot(arguments, output_mus, label='УДЭО')
plt.plot(arguments, output_mus_basic, label='ДЭО')
plt.legend()
plt.title('Интенсивность выходного потока. ' + info)
plt.xlabel('lambda')
plt.ylabel('mu')
plt.show()

plt.plot(arguments, total_delays, label='УДЭО')
plt.plot(arguments, total_delays_basic, label='ДЭО')
plt.legend()
plt.title('Общее время работы канала. ' + info)
plt.xlabel('lambda')
plt.ylabel('time')
plt.show()
