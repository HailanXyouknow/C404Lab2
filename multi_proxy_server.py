#!/usr/bin/env python3
import socket
from multiprocessing import Process

HOST = '' # reachable by any address the machine happens to have
PORT = 8001
BUFFER_SIZE = 1024

# create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except(socket.error, msg):
        print(f'Failed to create socket.')
        print('Error: {msg}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host info
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f'Host name is invalid: {host}')
        sys.exit()
    
    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print(f'Sending data')
    try:
        serversocket.sendall(payload)
    except socket.error:
        print(f'Could not send {payload}')
    print('Payload sent successfully')

def pass_data_between_proxy_client(conn, addr):
    url = "www.google.com"
    request = f"GET / HTTP/1.1\nHost: {url}\n\n"
    port = 80
    buffer_size = 4096

    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    print(f"Data received:", full_data)

    # Send data to Google if received any
    if full_data:
        # Connect to Google
        try:
            s2 = create_tcp_socket()
            remote_ip = get_remote_ip(url)
            s2.connect((remote_ip, port))
        except Exception as e:
            print(f'Error: {e}')
        send_data(s2, full_data)
        s2.shutdown(socket.SHUT_WR)

    # Get response from Google
    full_data = b''
    while True:
        data = s2.recv(buffer_size)
        if not data:
            break
        full_data += data
    #print(f'Response: \n{full_data}')

    # Send data back to connected client
    conn.sendall(full_data)
    print('Response from server is sent to client')
    conn.close()

def main():
    processes = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(10)
        except:
            for p in processes:
                p.join()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5) # maximum number of queued connections

        while True:
            # Get incoming data
            conn, addr = s.accept()
            p = Process(target=pass_data_between_proxy_client, args=(conn, addr))
            processes.append(p)
            p.start()

if __name__ == "__main__":
    main()
