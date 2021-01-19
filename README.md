# CMPUT 404 Lab 2

```bash
# TCP Socket library implementation
# Client:
./client.py

# Server:
./echo_server.py
# In another terminal run:
echo "hi" | nc localhost 8001 [-q 1]

# Proxy Server and Client:
# Server exits after 30 seconds to avoid hanging
./proxy_server.py 
# In another terminal run:
./proxy_client.py
```