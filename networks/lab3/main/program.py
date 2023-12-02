# lab03 networks

import random
window_quantity = 1000

def generate_poisson(lam):
    x = 0
    p = math.exp(-lam)
    u = random.random()
    while u > p:
        x += 1
        p += math.exp(-lam) * (lam**x) / math.factorial(x)
    return x

def message_will_be_sent(probability, window_width=None):
    if window_width != None:
        return True
    else:
        if random.random() > 0.5:
            return True
        return False
    
def generate_message(input_lambda):
    if random.random() > 0.5:
        return True
    return False

def model(subscriber_quantity, input_lambda, queue_size=None):
    subscribers_delay = [] # хранятся сообщения, которые в очереди 
    send_messages = [] # хранятся задержки отправленных сообщений
    for _ in range(subscriber_quantity):
        subscribers_delay.append([])
        send_messages.append([])
    
    wishing_send_amount = [] # хранится количество пользователей, захотевших отправить сообщение в текущем окне

    for current_window in range(window_quantity):
        current_queue = [] # номера пользователей, захотевших отправить сообщение

        for subscriber in range(subscriber_quantity):
            if len(subscribers_delay[subscriber]) != 0 and message_will_be_sent(0.0):
                current_queue.append(subscriber)
        wishing_send_amount.append(len(current_queue))
        
        if wishing_send_amount[-1] == 0: #пусто
            pass
        elif wishing_send_amount[-1] == 1: #успех
            messager_number = current_queue[0]
            send_messages[messager_number].append(subscribers_delay[messager_number][0])
            subscribers_delay[messager_number].pop(0)
        else: #конфликт
            pass

        # генерация сообщений
        for current_subscriber in subscribers_delay:
            if queue_size == None or len(current_subscriber) < queue_size:
                if generate_message(input_lambda):
                    current_subscriber.append(0)
        
        for subscriber in subscribers_delay:
            for message in range(len(subscriber)):
                subscriber[message] += 1
    
    # average_delay = 0
    # average_subsribers = 0
    # output_mu = 0
    # return [average_delay, average_subsribers, output_mu]
    print(wishing_send_amount)
    print(subscribers_delay[0])
    print(subscribers_delay[1])
    print(send_messages[0])
    print(send_messages[1])
    return True

model(2, 0.4, None)

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
