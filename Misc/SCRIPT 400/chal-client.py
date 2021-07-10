from pwn import *

RHOST = '127.0.0.1'
RPORT = 42069

conn = remote(RHOST, RPORT)

for i in range(4):
	data = conn.recvuntil("\n")
	print(data)

	eq = conn.recvuntil("=")
	eq = eq.decode()
	eq = eq[:-2]
	print(eq) 

	ans = str(eval(eq))
	print(ans)

	conn.sendline(ans)

conn.interactive()