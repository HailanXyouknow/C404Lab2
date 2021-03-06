#!/usr/bin/env python3
import socket, sys

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
        serversocket.sendall(payload.encode())
    except socket.error:
        print(f'Could not send {payload}')
    print('Payload sent successfully')

def main():
    url = "www.google.com"
    request = f"GET / HTTP/1.1\nHost: {url}\n\n"
    port = 80
    buffer_size = 4096

    try:
        s = create_tcp_socket()
        remote_ip = get_remote_ip(url)
        s.connect((remote_ip, port))
        send_data(s, request)
        s.shutdown(socket.SHUT_WR)

        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            full_data += data
        print(f'Response: \n{full_data}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        s.close

if __name__ == "__main__":
    main()
