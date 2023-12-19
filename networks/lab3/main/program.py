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


def poisson_stream(input_lambda): # сколько сообщений появилось в новом окне
    messages_count = 0
    exp = math.exp(-input_lambda)
    random_int = random.random()
    while random_int > exp:
        messages_count += 1
        exp += math.exp(-input_lambda) * (input_lambda**messages_count) / math.factorial(messages_count)
    return messages_count

# def message_will_be_sent_aloha(probability, window_width=None):
#     if window_width != None:
#         return True
#     else:
#         if random.random() > (1 - probability):
#             return True
#         return False
    
def message_will_be_sent_interval(current_window, stats):
    if stats['window_number'] == current_window or stats['window_number'] == 0:
        return True 
    return False

def model(subscriber_quantity, input_lambda, queue_size=None):
    subscribers_delay = [] # хранятся сообщения, которые в очереди 
    send_messages = [] # хранятся задержки отправленных сообщений
    subscriber_stats = [] # хранится ширина окна и номер выбранного окна абонента
    message_amount = []
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
        
        if wishing_send_amount[-1] == 0: # пусто
            pass
        elif wishing_send_amount[-1] == 1: # успех
            messager_number = current_queue[0]
            send_messages[messager_number].append(subscribers_delay[messager_number][0])
            subscribers_delay[messager_number].pop(0)
            subscriber_stats[messager_number]['width'] = w_min
            if len(subscribers_delay[messager_number]) != 0:
                subscriber_stats[messager_number]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[messager_number]['width'])
        else: # конфликт
            for subscriber in current_queue:
                subscriber_stats[subscriber]['width'] = min(subscriber_stats[subscriber]['width'] * 2, w_max)
                subscriber_stats[subscriber]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[subscriber]['width'])

        messages_count = poisson_stream(input_lambda)
        
        for _ in range(messages_count):
            subscriber_number = random.SystemRandom().randint(0, subscriber_quantity - 1)
            if queue_size == None or len(subscribers_delay[subscriber_number]) < queue_size:
                if len(subscribers_delay[subscriber_number]) == 0:
                    subscriber_stats[subscriber_number]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[subscriber]['width'])
                subscribers_delay[subscriber_number].append(0)
        
        for subscriber in subscribers_delay:
            for message in range(len(subscriber)):
                subscriber[message] += 1
    
    average_delay = 0 # сумма всех чисел из send_messages поделенная на len(send_mes)
    output_mu = 0 # len(send_mes)/количество окон
    for i in range(len(send_messages)):
        average_delay += sum(send_messages[i])
        output_mu += len(send_messages[i])
    if output_mu == 0:
        average_delay = 0
    else:
        average_delay = average_delay / output_mu
    output_mu = output_mu / window_quantity
        
    # average_subscribers = 0 # среднее из wishing_send_amount
    # average_subscribers = sum(wishing_send_amount) / len(wishing_send_amount)

    average_message_amount = sum(message_amount) / len(message_amount)
    
    return [average_delay, average_message_amount, output_mu]
    # return [average_delay, average_subscribers, output_mu]

average_delays = []
average_subscribers = []
output_mus = []
arguments = []

for _ in range(int(1.0 * precision)):
    result = model(M, input_lambda, queue_size)
    average_delays.append(result[0])
    average_subscribers.append(result[1])
    output_mus.append(result[2])
    arguments.append(input_lambda)
    input_lambda += 1 / precision
print("lambda = " + str(input_lambda))
print("average_delays = " + str(average_delays))
print("average_subscribers = " + str(average_subscribers))
print("output_mus = " + str(output_mus))

# average_delays_md1 =  [0, 1.0573203013642842, 1.1249752426223014, 1.218532334202621, 1.3329090228378884, 1.493138610092754, 1.7612452139170967, 2.137140385031365, 3.0031765562614567, 5.614859028592944]
# average_subscribers_md1 =  [0, 0.10385, 0.2272, 0.36913, 0.53403, 0.74535, 1.05804, 1.48202, 2.39193, 5.07037]
# output_mus_md1 =  [0, 0.09822, 0.20196, 0.30293, 0.40065, 0.49917, 0.6007, 0.69345, 0.79646, 0.90302]

info = "M=" + str(M) + ",QSIZE=" + str(queue_size) + " (W_MIN=" + str(w_min) + ",W_MAX=" + str(w_max) + ")"
plt.plot(arguments, average_delays, label='ДЭО')
# plt.plot(arguments, average_delays_md1, label='MD1')
plt.legend()
plt.title('Средняя задержка. ' + info)
plt.xlabel('lambda')
plt.ylabel('d(lambda)')
plt.show()


plt.plot(arguments, average_subscribers, label='ДЭО')
# plt.plot(arguments, average_subscribers_md1, label='MD1')
plt.legend()
plt.title('Среднее количество сообщений. ' + info)
plt.xlabel('lambda')
plt.ylabel('N')
plt.show()

plt.plot(arguments, output_mus, label='ДЭО')
# plt.plot(arguments, output_mus_md1, label='MD1')
plt.legend()
plt.title('Интенсивность выходного потока. ' + info)
plt.xlabel('lambda')
plt.ylabel('mu')
plt.show()

