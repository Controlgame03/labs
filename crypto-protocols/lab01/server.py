import socket
import random
import utils
import threading
import time

CLIENT_AMOUNT = 2

passwordLibrary = {
    'user_1': '123456789',
    'user_2': 'qwerty',
    'user_3': '0000'
}

p = 997
g = 7

def handleClient(conn):
    username = conn.recv(1024).decode()
    if username in passwordLibrary:
        conn.send('OK'.encode())
    else:
        conn.send('User is not found'.encode())
        conn.close()
        return
    timeStart = time.time()
    x1_A = random.randint(1, p - 1)
    x2_A = random.randint(1, p - 1)
    y1_A = utils.mod_exp(g, x1_A, p)
    y2_A = utils.mod_exp(g, x2_A, p)

    while y2_A == 1:
        x2_A = random.randint(1, p - 1)
        y2_A = utils.mod_exp(g, x2_A, p)
  
    y1_A_received = int(conn.recv(1024).decode())
    conn.send(str(y1_A).encode())

    y2_A_received = int(conn.recv(1024).decode())
    conn.send(str(y2_A).encode())

    h_A = utils.hash_password(passwordLibrary[username]) % p
    alice = utils.mod_exp((y1_A * y1_A_received * y2_A_received) % p, (x2_A * h_A), p)
    bob = int(conn.recv(1024).decode())
    
    num_to_reverse = utils.mod_exp(y2_A_received, x2_A * h_A, p)
    a_reverse = utils.getReverseNumber(num_to_reverse, p)

    alice_received = utils.mod_exp((bob * a_reverse) % p, x2_A, p)
    conn.send(str(alice).encode())

    received_hash_key = conn.recv(1024).decode()
    conn.send(str(utils.hash_password(str(alice_received))).encode())

    if str(utils.hash_password(str(alice_received))) == received_hash_key:
        print("Session keys matched. Key exchange successful. (", (time.time() - timeStart), ')')
    else:
        conn.close()
        return
            
    while True:
        data = conn.recv(1024)
        print('Request[', username, '] =: ', data.decode())
        if not data:
            break
        
        conn.send('data'.encode())
    conn.close()

def server_program():
    host = socket.gethostname()
    print('Host`s name: ', host)
    port = 5001
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(CLIENT_AMOUNT)
    
    abonentThreads = []
    for _ in range(CLIENT_AMOUNT):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        conThread = threading.Thread(target=handleClient, args=(conn,))
        conThread.start()
        abonentThreads.append(conThread)
    
    for i in range(CLIENT_AMOUNT):
        abonentThreads[i].join()


if __name__ == '__main__':
    server_program()
