#!/usr/bin/env python3
# echo "hi" | nc localhost 8001
import socket
import time

URL = 'www.google.com'
HOST = '' # reachable by any address the machine happens to have
PORT = 8001
BUFFER_SIZE = 1024

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

def main():
    # socket.socket() supports context manager type
    # thus no need to call s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2) # maximum number of queued connections

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            full_data = conn.recv(BUFFER_SIZE)
            print(f"Data received:", full_data)
            time.sleep(0.5)
            conn.sendall(full_data)
            conn.close()

if __name__ == "__main__":
    main()
