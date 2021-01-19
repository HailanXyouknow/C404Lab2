#!/usr/bin/env python3
import socket, sys

HOST = '127.0.0.1' # Server's hostname or IP
PORT = 8001 # Port used by Server

def main():
    url = 'www.google.com'
    request = f"GET / HTTP/1.1\nHost: {url}\n\n"
    port = 80
    buffer_size = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            full_data += data
        print(f'Response: \n{full_data}')

if __name__ == "__main__":
    main()
