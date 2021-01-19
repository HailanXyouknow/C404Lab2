#!/usr/bin/env python3
# echo "hi" | nc localhost 8001
import socket
from multiprocessing import Process
import time

HOST = '' # reachable by any address the machine happens to have
PORT = 8001
BUFFER_SIZE = 1024
MAX_CONNECTIONS = 10

def echo(conn, addr):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    print(f"Data received:", full_data)
    conn.sendall(full_data)
    print(f"Data is sent to:", addr)
    time.sleep(0.5)
    conn.close()

def main():
    # socket.socket() supports context manager type
    # thus no need to call s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # allow reused addresses
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(MAX_CONNECTIONS) # maximum number of queued connections

        while True:
            conn, addr = s.accept()
            p = Process(target=echo, args=(conn, addr))
            p.daemon = True
            p.start()
            print(f"Started Process {p}")
            p.join()
       
        
if __name__ == "__main__":
    main()
