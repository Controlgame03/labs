# lab03 networks

import random
import math

window_quantity = 10000
input_lambda = 0.2
# probability = 0.5
M = 2
w_min = 2
w_max = 64


def poisson_stream(input_lambda): # сколько сообщений появилось в новом окне
    messages_count = 0
    exp = math.exp(-input_lambda)
    random_int = random.random()
    while random_int > exp:
        messages_count += 1
        exp += math.exp(-input_lambda) * (input_lambda**messages_count) / math.factorial(messages_count)
    return messages_count

def message_will_be_sent_aloha(probability, window_width=None):
    if window_width != None:
        return True
    else:
        if random.random() > (1 - probability):
            return True
        return False
    
def message_will_be_sent_interval(current_window, stats):
    if stats['window_number'] == current_window or stats['window_number'] == 0:
        return True 
    return False

def model(subscriber_quantity, input_lambda, queue_size=None):
    subscribers_delay = [] # хранятся сообщения, которые в очереди 
    send_messages = [] # хранятся задержки отправленных сообщений
    subscriber_stats = [] # хранится ширина окна и номер выбранного окна абонента
    for _ in range(subscriber_quantity):
        subscribers_delay.append([])
        send_messages.append([])
        subscriber_stats.append(dict(width=w_min, window_number=0))
    
    wishing_send_amount = [] # хранится количество пользователей, захотевших отправить сообщение в текущем окне

    for current_window in range(window_quantity):
        current_queue = [] # номера пользователей, захотевших отправить сообщение

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
            subscriber_stats[messager_number]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[messager_number]['width'])
        else: # конфликт
            for subscriber in current_queue:
                subscriber_stats[subscriber]['width'] = min(subscriber_stats[subscriber]['width'] * 2, w_max)
                subscriber_stats[subscriber]['window_number'] = current_window + random.SystemRandom().randint(1, subscriber_stats[subscriber]['width'])

        messages_count = poisson_stream(input_lambda)
        
        for _ in range(messages_count):
            subscriber_number = random.SystemRandom().randint(0, subscriber_quantity - 1)
            if queue_size == None or len(subscribers_delay[subscriber_number]) < queue_size:
                subscribers_delay[subscriber_number].append(0)
        
        for subscriber in subscribers_delay:
            for message in range(len(subscriber)):
                subscriber[message] += 1
    
    # average_delay = 0
    # average_subsribers = 0
    # output_mu = 0
    # return [average_delay, average_subsribers, output_mu]
    # print(wishing_send_amount)
    # print(subscribers_delay[0])
    # print(subscribers_delay[1])
    # print(send_messages[0])
    # print(send_messages[1])
    print(subscribers_delay[0])
    print(subscribers_delay[1])
    return True

model(M, input_lambda, None)

# queue_size = None
# M = 2
# precision = 10

# average_delays = []
# average_subscribers = []
# output_mus = []
# current_lambda = 0

# for _ in range(precision):
#     result = model(M, current_lambda, queue_size)
#     average_delays.append(result[0])
#     average_subscribers.append(result[1])
#     output_mus.append(result[2])

#     current_lambda += 1 / precision

# print("average_delays = " + str(average_delays))
# print("average_subscribers = " + str(average_subscribers))
# print("output_mus = " + str(output_mus))




# 12.02 переделать программу без выделения очереди для каждого пользователя
# с помощью метода generate_poisson(lam)
# 12.03 переделать программу и исправить генерацию windiw_number в словаре stats
