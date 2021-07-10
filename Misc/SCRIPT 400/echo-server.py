import socket

LHOST = '127.0.0.1'
LPORT = 42069       

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((LHOST, LPORT))
s.listen()

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr[0]}")
    data = conn.recv(1024)

    if not data:
        break
    else:
        print(f"Message to echo: {data}")

    conn.sendall(data)
    conn.close()