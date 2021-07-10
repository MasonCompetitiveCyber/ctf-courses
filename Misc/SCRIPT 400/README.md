<h1 align="center">SCRIPT 400</h1>
  <p align="center">
     Python: Interacting w/ Sockets
  </p>

### Table of contents

- [Prerequisites](#prerequisites)
- [Introduction](#introduction)
- [Python Sockets](#python-sockets)
- [`pwntools` remote](#pwntools-remote)
  - [Setup](#setup)
  - [Client Code](#client-code)
- [Challenge](#challenge)
- [Next Steps](#next-steps)
- [More Resources](#more-resources)
- [Creators](#creators)

## Prerequisites
- Scripting 200
  - You should be comfortable with basic python programming (if/else, loops, functions)
- Scripting 300
  - You should be comfortable with using some more advanced python functions
- Scripting 310
  - You should be comfortable with using 3rd-party libraries

## Introduction
This course will introduce you to using Python to communicate with remote endpoints. You will encounter challenges that are hosted on a remote IP address and port, so you must be able to connect to it to recieve and send data. We will discuss two main ways to do so. The first is using Python's built-in socket programming library, and the second is using a third-party library called `pwntools` (usually used for binary exploitation challenges, but are also helpful for basic remote comms as well).

## Python Sockets
Sockets allow for linking communication between two different processes over a network. In our case, the two parties communicating will be the challenge, and you, the player. To learn the basics of how we can send and receive data from a remote endpoint, we will look at a very simple example. The following code will be for the server we will be communicating with ([echo-server.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20400/echo-server.py)):
```python
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
```
So what does this do? Let's break it down. Our first steps are to import the `socket` library and to set a variable to hold the IP address and port we will be running the server on (`LHOST` and `LPORT`). Since we will be running these locally, we should use the localhost address, and the port can be whatever we want (as long as it's not a commonly used port number). Next, we see some funky stuff. First, we have:
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
`socket.socket()` will create our socket object. The first parameter, `socket.AF_INET`, is telling the socket that we are going to use IPv4. The second paramter, `socket.SOCK_STREAM`, is telling the socket to use TCP instead of UDP (which is `sock.SOCK_DGRAM`). Next we see this:
```python
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
`s.setsockopt()` is mean to set values for certain socket options. I will start with the second parameter, `socket.SO_REUSEADDR`, which is the name of the option we want to set that allows us to reuse a socket before it has fully timed-out. This is useful because if you stop running the server, the socket you are using on the IP/port you specified will be left in a `TIME_WAIT` state and can't be reaused until it has naturally timed out. Instead of waiting for this timeout to start running the server again, we can set the option `SO_REUSEADDR` to tell the socket it is okay to start using a socket that hasn't fully timed out. If you want to read the official docs for it, it's at the very bottom of https://docs.python.org/3/library/socket.html. The third argument, `1`, is setting the value of the option to True. The first argument, `socket.SOL_SOCKET`, is setting the "level" of the option, which in this case is telling the socket to search for this option in the socket itself. Don't ask me what this means, I really don't know. Let's move on to the more fun stuff:
```python
s.bind((LHOST, LPORT))
s.listen()
```
The first line is telling the socket to bind itself to the IP address and port provided. The second line is telling the socket to start "listening" on the address it just bound to. Now the final block of code:
```python
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
```
In the while loop, the first thing that happens is we assign to variables, `conn` and `addr` to the result of `s.accept()`. This `accept` function will block further program execution until it receives a connection on the address it's listening on. When a client connects to it, it will return another socket object to handle the connection (which we save into the variable `conn`) and a tuple containing the IP and port of the client (which we save into the variable `addr`). We then print out the IP address of the client for logging purposes. 

We then use `conn.recv(1024)` to receive up to 1024 bytes of data from our socket connection and put it into `data`. We then check that we received data before printing it out. Finally, we send the data we received back to the client over our connection using `conn.sendall(data)` and close the connection with `conn.close()`. Because this is all running in a while loop, we can receive another connection after the first one closes, and so on. We can just use `ctrl+c` from the CLI to stop it when we want to.

Overall, the server code is accepting a connection, receiving data from the client, sending it back to them, closing the connection, and then waiting for a new connection. Now let's move on to the client code to interact with the server:
```python
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
```
Let's run through this a bit faster now. We set variables RHOST and RPORT that denote the address of the socket we want to connect to (these should be the ones the server is binding and listening on). We then create our socket object and connect to the socket with `s.connect()`. We then encode our message "Hello there!" because the socket communications (receiving and sending data) has to be in bytes. We then send our message (now in bytes) using `s.sendall()`. We then receive the server's response and print out the decoded data (we are given a response in bytes, as mentioned before, so we need to convert it to a normal string) and close the connection with `s.close()`. 

Now let's run it! In one terminal window, run `python3 echo-server.py`. You should see that it's just hanging. This is because it's waiting for a connection. To check that it's running, you can open up a new terminal window and run:
```console
$ lsof -i :42069 
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 55365 root    3u  IPv4 553083      0t0  TCP localhost:42069 (LISTEN)

OR

$ netstat -ltnp | grep 42069
tcp        0      0 127.0.0.1:42069         0.0.0.0:*               LISTEN      55365/python3       
```
Now let's run the client with `python3 echo-client.py`. We should we this output on the server:
```console
$ python3 echo-server.py  
Connection from 127.0.0.1
Message to echo: b'Hello there!'
```
and this output on the client:
```console
$ python3 echo-client.py
Hello there
```
Awesome!

## `pwntools` remote
In the previous section, we used Python's socket library to interact with the server. We can also do the same thing using `pwntools`. 

### Setup
The first thing you'll need to do is install pwntools, by running `$ pip3 install pwntools`. You can check that it installed by running `$ pwn`. You should see output that looks something like this:
```console
$ pwn
[*] Checking for new versions of pwntools
    To disable this functionality, set the contents of /root/.cache/.pwntools-cache-3.9/update to 'never' (old way).
    Or add the following lines to ~/.pwn.conf or ~/.config/pwn.conf (or /etc/pwn.conf system-wide):
        [update]
        interval=never
[*] You have the latest version of Pwntools (4.5.1)
usage: pwn [-h]

{asm,checksec,constgrep,cyclic,debug,disasm,disablenx,elfdiff,elfpatch,errnohex,phd, pwnstrip,scramble,shellcraft,template,unhex,update,version}
```

### Client Code
Let's start by looking at the code and breaking it down ([pwn-client.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20400/pwn-client.py)):
```python
from pwn import *

RHOST = '127.0.0.1'
RPORT = 42069

conn = remote(RHOST, RPORT)

msg = "Hello there!".encode()
conn.sendline(msg)

data = conn.recvline()
print(data.decode())

conn.close()
```
You can probably see that this is very similar to using python sockets. The biggest visible difference here is that we use `remote()` to create a connection instead of creating a socket and connecting to the socket as we had done with the echo client. We are then using `sendline()` to send our message and `recvline()` to recieve the data being sent back to us. Let's see what happens when we run it:
```console
$ python3 pwn-client.py 
[+] Opening connection to 127.0.0.1 on port 42069: Done
Hello there!

[*] Closed connection to 127.0.0.1 port 42069
```
It works! And we have the bonus of some very nice looking log statements.

Here are the methods we have available to us for sending and receiving data:

Receiving data
- `recv(n)` - Receive any number of available bytes
- `recvline()` - Receive data until a newline is encountered
- `recvuntil(delim)` - Receive data until a delimiter is found
- `recvregex(pattern)` - Receive data until a regex pattern is satisfied
- `recvrepeat(timeout)` - Keep receiving data until a timeout occurs
- `clean()` - Discard all buffered data

Sending data
- `send(data)` - Sends data
- `sendline(line)` - Sends data plus a newline

I personally find the `recvuntil(delim)` very useful, I'll show you quickly how it works. Let's take the same code as before, but modify it slightly, like so:
```python
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
```
Since we know the data we're receiving, we can now specify what data we want to receive using `recvuntil(delim)`. I know that the word "Hello" is being sent, so we can receive data until we hit the "o". This should give us "Hello". Then we receive until the "!", so we should get " there!". Notice the space in the front, this is because we are continuing receiving data right after the "Hello", which starts with a space. Let's run it and see what happens:
```console
$ python3 pwn-client.py
[+] Opening connection to 127.0.0.1 on port 42069: Done
Hello
 there!
[*] Closed connection to 127.0.0.1 port 42069
```
Just what we expected! 

## Challenge
We are now ready to solve a simple challenge. I will not be going over the server code, but you can try to look over it and understand it yourself, if you want to. The server code is [chal-server.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20400/chal-server.py). We can see what this does by running it in one terminal and connecting to it using netcat from another. Example output:
```console
$ nc localhost 42069
What's the answer to the following math problem?
5-18 = 

Too slow! 
```
So we are asked to solve a math problem, but we don't have much time to respond before it ends our connection. You can keep running some tests and you will see that the connection will end if you take more than 2 seconds to answer or provide the wrong answer. If you get past 5 questions in a row, you will get the flag. Now, this is not impossible to do by hand, you might get 5 easy questions you can do quickly in your head. But that's not the point. The challenge could have set the timer to 1 second instead, and then it would be impossible, or had harder equations. 

We can see now, that the best way to solve this is using a python script to read in the equation and send back the correct answer. Let's start working on it.

Let's use `pwntools` for this. Here is our first step:
```python
from pwn import *

RHOST = '127.0.0.1'
RPORT = 42069

conn = remote(RHOST, RPORT)

d = conn.recvuntil("\n")
print(d)
```
We are connecting to the server and then receiving data until the first new line and printing everything we recieved out. We hope to see `What's the answer to the following math problem?`, as that is the first thing we are sent by the server and it ends in a new line before giving us the equation. Here's the output:
```console
$ python3 chal-client.py
[+] Opening connection to 127.0.0.1 on port 42069: Done
b"What's the answer to the following math problem?\n"
[*] Closed connection to 127.0.0.1 port 42069
```
Perfect. Now we want to receive until the equals sign to get our equation out (I will leave out chunks of code and replace it with \<snip\> to save visual space):
```python
<snip>

data = conn.recvuntil("\n")

eq = conn.recvuntil("=")
print(eq)
```
```console
$ python3 chal-client.py
[+] Opening connection to 127.0.0.1 on port 42069: Done
b'2+13 ='
[*] Closed connection to 127.0.0.1 port 42069
```
We get the equation in our output, however, we don't want the extra space and equals sign, we just want the raw equation, so just `2+13`. This is because we can use Python's `eval()` function to evaluate the string "2+13" and give us back the answer, which would be 15, like so:
```python
>>> eval("2+13")
15
```
Let's get that working.
```python
<snip>

eq = conn.recvuntil("=")
eq = eq.decode()
eq = eq[:-2]
print(eq)

ans = str(eval(eq))
print(ans)
```
We are decoding the data we receive, since it's in bytes and taking off the last two characters (the space and equals sign). Then we run it through `eval()` and convert it to a string (`eval` will output an integer). Let's see what we get:
```console
$ python3 chal-client.py
[+] Opening connection to 127.0.0.1 on port 42069: Done
2*14
28
[*] Closed connection to 127.0.0.1 port 42069
```
Perfect! Now all we have to do is send this data back, and loop it!
```python
from pwn import *

RHOST = '127.0.0.1'
RPORT = 42069

conn = remote(RHOST, RPORT)

while True:
	data = conn.recvuntil("\n")
	print(data)

	eq = conn.recvuntil("=")
	eq = eq.decode()
	eq = eq[:-2]
	print(eq) 

	ans = str(eval(eq))
	print(ans)

	conn.sendline(ans)
```
The only addition to this script is using `sendline` to send our answer and putting everything in an infinite loop. Let's see what happens:
```console
$ python3 chal-client.py
[+] Opening connection to 127.0.0.1 on port 42069: Done
b"What's the answer to the following math problem?\n"
0*7
0
b" What's the answer to the following math problem?\n"
18*8
144
b" What's the answer to the following math problem?\n"
8-18
-10
b" What's the answer to the following math problem?\n"
8-4
4
b" What's the answer to the following math problem?\n"
7*16
112
b' \n'
Traceback (most recent call last):
  File "/root/Documents/masoncc/misc/scripting/chal-client.py", line 12, in <module>
    eq = conn.recvuntil("=")
  File "/usr/local/lib/python3.9/dist-packages/pwnlib/tubes/tube.py", line 333, in recvuntil
    res = self.recv(timeout=self.timeout)
  File "/usr/local/lib/python3.9/dist-packages/pwnlib/tubes/tube.py", line 105, in recv
    return self._recv(numb, timeout) or b''
  File "/usr/local/lib/python3.9/dist-packages/pwnlib/tubes/tube.py", line 183, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
  File "/usr/local/lib/python3.9/dist-packages/pwnlib/tubes/tube.py", line 154, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
  File "/usr/local/lib/python3.9/dist-packages/pwnlib/tubes/sock.py", line 58, in recv_raw
    raise EOFError
EOFError
[*] Closed connection to 127.0.0.1 port 42069
```
It looks like we got through 5 problems but then we don't get another problem, just what looks like a space and a newline, and then we hit an end-of-file error. Instead of the infinite loop, let's run it 5 times and then see what we get.
```python
from pwn import *

RHOST = '127.0.0.1'
RPORT = 42069

conn = remote(RHOST, RPORT)

for i in range(5):
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
```
The main difference other than the for loop, is the last line `conn.interactive()`. This lets us *interact* with the connection, which basically means it will end the scripts' control over the connection and hand it over to us. This will look similar to how we interface with the connection over netcat. Here's the output:
```console
python3 chal-client.py
[+] Opening connection to 127.0.0.1 on port 42069: Done
b"What's the answer to the following math problem?\n"
10-13
-3
b" What's the answer to the following math problem?\n"
15*20
300
b" What's the answer to the following math problem?\n"
6+3
9
b" What's the answer to the following math problem?\n"
2+14
16
b" What's the answer to the following math problem?\n"
19-19
0
[*] Switching to interactive mode
 

flag{qu1ck_m4ths}
[*] Got EOF while reading in interactive
```
We got a flag!

You might have noticed that we didn't end up having any interactive control, but that is because before we had the chance to, the connection closed after spitting out the flag. You can better understand what's happening if you make the for loop go 4 times instead of 5, so it will end up spitting you out to answer the 5th question. 

## Next Steps
 - make [chal-client.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20400/chal-client.py) more versatile 

## More Resources
- https://realpython.com/python-sockets/
- https://docs.python.org/3/library/socket.html
- https://docs.python.org/3/howto/sockets.html
- https://www.tutorialspoint.com/python/python_networking.htm
- https://docs.pwntools.com/en/stable/intro.html
- https://github.com/Gallopsled/pwntools-tutorial/blob/master/tubes.md
- https://es7evam.gitbook.io/security-studies/exploitation/sockets/03-connections-with-pwntools

## Creators

**Daniel Getter**

Enjoy :metal: