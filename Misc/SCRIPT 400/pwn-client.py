from pwn import *

RHOST = '127.0.0.1'
RPORT = 42069

conn = remote(RHOST, RPORT)

msg = "Hello there!".encode()
conn.sendline(msg)

# data = conn.recvline()
# print(data.decode())

hello = conn.recvuntil("o")
print(hello.decode())

there = conn.recvuntil("!")
print(there.decode())

conn.close()
