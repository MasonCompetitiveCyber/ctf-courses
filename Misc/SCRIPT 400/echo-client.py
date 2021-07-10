import socket

RHOST = '127.0.0.1'
RPORT = 42069

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

msg = "Hello there!".encode()
s.sendall(msg)

data = s.recv(1024)
print(data.decode())
s.close()