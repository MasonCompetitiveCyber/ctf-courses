import socket
from random import randint
import time
import signal

def timeout_handler(signum, frame):
    raise TimeoutError 

signal.signal(signal.SIGALRM, timeout_handler)

LHOST = '127.0.0.1'
LPORT = 42069       

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((LHOST, LPORT))
s.listen()

def make_eq():
    operations = ['+', '-', '*']

    first_num = str(randint(0,20))
    second_num = str(randint(0,20))
    operation = operations[randint(0,2)]

    eq = first_num + operation + second_num
    ans = str(eval(eq))

    return eq, ans

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr[0]}")

    win = True
    for i in range(5):
        eq, ans = make_eq()
        prompt = "What's the answer to the following math problem?\n"
        prompt += eq + " = "
        conn.sendall(prompt.encode())
        try:
            signal.alarm(2)
            data = conn.recv(1024)
            signal.alarm(0)

            data = data.decode()
            data = data.strip()

            if data != ans:
                conn.sendall(b"\nYou should brush up on your math!\n")
                conn.close()
                win = False
                break
        except TimeoutError:
            conn.sendall(b"\nnToo slow!\n")
            conn.close()
            win = False
            break
            
    if win:
        conn.sendall(b"\n\nflag{qu1ck_m4ths}\n")
        conn.close()
    