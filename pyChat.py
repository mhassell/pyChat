import threading
import socket

# initialize socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
printLock = threading.Lock()

def listen(conn, addr):
    done = False
    while ~done:
        data = conn.recv(4096)
        if data!='EOF':
            with printLock:
                print(addr + ': ' + data)
        else:
            done = True
    return
        

def send(conn):
    done = False
    while ~done:
        msg = raw_input()
        if msg!='QUIT':
            conn.sendall(msg)
        else:
            conn.sendall('EOF')
            done = True
    return

# inquire if the user wants to listen or connect:

mode = raw_input('Would you like to listen (L) or connect (C)? ')

if mode.upper() == 'L':
    
    ip = raw_input('Enter the IP address you would like to listen for: ')
    conn_socket = raw_input('Enter the socket you would like to listen on: ')

    accept_from = (ip, int(conn_socket))
    my_socket.bind(accept_from)
    my_socket.listen(1)
    conn, addr = my_socket.accept()
    with printLock:
        print('Client connected from ' + addr[0] +':'+str(addr[1]))
    listen_thread = threading.Thread(target=listen, args = (conn, addr[0]))
    send_thread = threading.Thread(target=send, args=(conn,))
    
else:
    ip = raw_input('Enter the IP address you would like to connect to: ')
    conn_socket = raw_input('Enter the socket you would like to connect to: ')
    
    my_socket.connect((ip, int(conn_socket)))
    with printLock:
        print('Connected to ' + ip +':'+ conn_socket)
    listen_thread = threading.Thread(target=listen, args = (my_socket, ip))
    send_thread = threading.Thread(target=send, args=(my_socket,))


listen_thread.start()
send_thread.start()
