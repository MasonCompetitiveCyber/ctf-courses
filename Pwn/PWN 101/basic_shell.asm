section .text ; Indicates that this is the text section
global _start ; Begins execution at _start label
_start:

mov rax, 59 ; Syscall for execve
mov rbx, 0 ; Sets rbx to NULL
push rbx ; Pushes a string terminator onto the stack
mov rbx, 0x68732f6e69622f ; Moves "/bin/sh" (written in ASCII) to rbx
push rbx ; Pushes "/bin/sh" onto the stack
mov rdi, rsp ; Get a pointer to "/bin/sh" in RDI
mov rsi, 0 ; Sets rsi to NULL
mov rdx, 0 ; Sets rdx to NULL
syscall ; Does the actual system interrupt
