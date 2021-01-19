#!/usr/bin/env python3
# echo "hi" | nc localhost 8001
import socket
from multiprocessing import Process

HOST = '' # reachable by any address the machine happens to have
PORT = 8001
BUFFER_SIZE = 1024
MAX_CONNECTIONS = 5

def echo_message(conn, addr):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    print(f"Data received:", full_data)
    conn.sendall(full_data)
    print(f"Data is sent to:", addr)
    conn.close()

def main():
    # socket.socket() supports context manager type
    # thus no need to call s.close()

    processes = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(10)
        except:
            for p in processes:
                p.join()

        # allow reused addresses
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(MAX_CONNECTIONS) # maximum number of queued connections
        while True:
            conn, addr = s.accept()
            p = Process(target=echo_message, args=(conn, addr))
            processes.append(p)
            p.daemon = True
            p.start()
            print(f"Started Process {p}")
        
if __name__ == "__main__":
    main()
