import socket
import random
import utils

p = 997
g = 7

def client_program():
    host = 'happy'
    port = 5001
    
    username = input('Username: ')
    

    client_socket = socket.socket()
    client_socket.connect((host, port))

    client_socket.send(str(username).encode())
    server_answer = client_socket.recv(1024).decode()
    print('Server: ', server_answer)
    if server_answer != 'OK':
        client_socket.close()
        return
    
    password = input('Password: ')

    x1_B = random.randint(1, p - 1)
    x2_B = random.randint(1, p - 1)
    y1_B = utils.mod_exp(g, x1_B, p)
    y2_B = utils.mod_exp(g, x2_B, p)

    while y2_B == 1:
        x2_B = random.randint(1, p - 1)
        y2_B = utils.mod_exp(g, x2_B, p)

    client_socket.send(str(y1_B).encode())
    y1_B_received = int(client_socket.recv(1024).decode())

    client_socket.send(str(y2_B).encode())
    y2_B_received = int(client_socket.recv(1024).decode())

    h_B = utils.hash_password(password) % p
    bob = utils.mod_exp((y1_B * y1_B_received * y2_B_received) % p, (x2_B * h_B), p)
    
    client_socket.send(str(bob).encode())
    
    num_to_reverse = utils.mod_exp(y2_B_received, x2_B * h_B, p)
    b_reverse = utils.getReverseNumber(num_to_reverse, p)
    
    alice = int(client_socket.recv(1024).decode())
    bob_received = utils.mod_exp((alice * b_reverse) % p, x2_B, p)

    client_socket.send(str(utils.hash_password(str(bob_received))).encode())
    received_hash_key = client_socket.recv(1024).decode()

    if str(utils.hash_password(str(bob_received))) == received_hash_key:
        print("Session keys matched. Key exchange successful.")
    else:
        print("Wrong password")
        client_socket.close()
        return

    message = input("-> ")
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024)
        print('Received from server: ' + data.decode())
        message = input('-> ')
    client_socket.close()


if __name__ == '__main__':
    client_program()
