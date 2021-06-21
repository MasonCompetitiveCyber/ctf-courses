<h1 align="center">PWN 100</h1>
  <p align="center">
  Integer Overflows
  </p>

### Table of contents

- [Introduction](#introduction)
- [Integer Limits](#integer-limits)
- [Integer Overflows](#integer-overflows)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction

Before talking about more complicated topics, such as buffer overflows or format string vulnerabilities, we will start off by discussing a very basic vulnerability: the integer overflow. Integer overflows are extremely common in programs that do some kind of math incorrectly, and they are usually caused when the programmer doesn't take into account the fact that the result could be outside the bounds of what he/she expects.

## Integer Limits

In any programming language, whenever we want to store some kind of number, the computer will allocate a certain number of bytes on the stack (or sometimes the heap) in order to store that variable. This is why when you declare `int x` in C, the compiler makes sure that enough bytes are allocated on the stack (usually two, four, or eight bytes) in order to store a single integer. The `int` type specifier that comes before the variable name is necessary to write out because it dictates how much memory is supposed to be allocated on the stack.

Because the computer has a limited number of bytes that can be used to store the variable, there are always upper and lower bounds for the number that can be stored. If four bytes are used to store an unsigned integer, then that means that the maximum number that can be represented in that variable is `2^32 - 1 = 4294967295`, and the minimum number that can be represented is simply zero. If four bytes are used to store a two's complement signed integer, then that means that the maximum number that can be represented in that variable is `2^31 - 1 = 2147483647`, and the minimum number that can be represented is `-1 * 2^31 = -2147483648`. If this idea confuses you, then you may want to take a look at [this](https://www.tutorialspoint.com/two-s-complement) and [this](https://nickolasteixeira.medium.com/how-to-explain-to-my-wife-what-i-do-how-do-you-get-the-maximum-and-minimum-values-for-integer-befdc263a3a2).
```C
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main() {
    printf("Unsigned Integers (%u bytes): \n", sizeof(unsigned int));
    printf("Maximum value: %u\n", UINT_MAX);
    printf("Maximum value plus 1: %u\n", UINT_MAX+1);
    printf("Minimum value: %u\n", 0);
    printf("Minimum value minus 1: %u\n\n", 0-1);

    printf("Signed Integers (%u bytes): \n", sizeof(int));
    printf("Maximum value: %d\n", INT_MAX);
    printf("Maximum value plus 1: %d\n", INT_MAX+1);
    printf("Minimum value: %d\n", INT_MIN);
    printf("Minimum value minus 1: %d\n", INT_MIN-1);

    return 0;
}
```
Now, what would happen if we were to add one to the upper bound of a number or subtract one from the lower bound of a number in C? We can include the `limits.h` library in order to obtain the upper and lower bounds of integers and print them out, as shown in the code above. If we compile and run the code shown above, we get the below output (note that you may get some compiler warnings about integer overflows when you do this).
```bash
$ gcc -o int_overflow int_overflow.c
int_overflow.c: In function ‘main’:
int_overflow.c:14:49: warning: integer overflow in expression of type ‘int’ results in ‘-2147483648’ [-Woverflow]
   14 |     printf("Maximum value plus 1: %d\n", INT_MAX+1);
      |                                                 ^
int_overflow.c:16:50: warning: integer overflow in expression of type ‘int’ results in ‘2147483647’ [-Woverflow]
   16 |     printf("Minimum value minus 1: %d\n", INT_MIN-1);
      |                                                  ^

$ ./int_overflow
Unsigned Integers (4 bytes):
Maximum value: 4294967295
Maximum value plus 1: 0
Minimum value: 0
Minimum value minus 1: 4294967295

Signed Integers (4 bytes):
Maximum value: 2147483647
Maximum value plus 1: -2147483648
Minimum value: -2147483648
Minimum value minus 1: 2147483647
```
(The sizes of signed or unsigned integers vary, which may cause your computer to produce a different output than what is shown above.)
What's interesting about the above output is that whenever you add one to the maximum value, you get the minimum value, and whenever you subtract one from the minimum value, you get the maximum value. The program makes sure that the value is always within the upper and lower bounds, even if it does not make mathematical sense. The key takeaway here is that if a program does not check whether its inputs are within the upper and lower bounds, then it can be possible for an attacker to exploit the program. This is especially common when the programmer mixes up signed and unsigned numbers with each other.

## Integer Overflows
Let's say that we're given the following program:
```C
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    unsigned int money;
    int withdraw;
    char buf[50];

    money = 10;
    printf("Welcome to Vuln Bank!\nYour goal is to become a millionaire.\n");

    while(money < 1000000) {
        printf("You currently have $%u in your bank account.\n", money);
        printf("Enter the amount of money that you would like to withdraw: ");
        fgets(buf, 50, stdin);
        sscanf(buf, "%d", &withdraw);
        printf("Removing $%d from your account.\n", withdraw);
        money -= withdraw;
    }

    printf("You currently have $%u in your bank account.\n", money);
    printf("Congratulations! You\'re rich!");

    return 0;
}
```
This is a program that simulates a "bank" that contains $10 by default. It states that our goal is to become a millionaire, and this can only happen when the `money` variable is greater than 1,000,000. However, this banking application does not allow us to deposit money into our account; it only allows us to withdraw money. Here is what happens when we compile the program, run it, and give it some input values to withdraw:
```bash
$ gcc -o vuln_bank vuln_bank.c
$ ./vuln_bank
Welcome to Vuln Bank!
Your goal is to become a millionaire.
You currently have $10 in your bank account.
Enter the amount of money that you would like to withdraw: 1
Removing $1 from your account.
You currently have $9 in your bank account.
Enter the amount of money that you would like to withdraw: 2
Removing $2 from your account.
You currently have $7 in your bank account.
Enter the amount of money that you would like to withdraw: 3
Removing $3 from your account.
You currently have $4 in your bank account.
Enter the amount of money that you would like to withdraw: 4
Removing $4 from your account.
You currently have $0 in your bank account.
Enter the amount of money that you would like to withdraw:
```
One thing that you should immediately notice in the code is that the `money` variable is unsigned, but the `withdraw` variable, which is being subtracted from `money`, is signed. Usually, whenever a mathematical operation occurs between a signed and an unsigned number, there is a good chance that the programmer did something incorrect and caused an integer overflow vulnerability to appear. In this example, we are actually able to withdraw negative amounts of money because the programmer did not check for negatives.
```bash
$ ./vuln_bank
Welcome to Vuln Bank!
Your goal is to become a millionaire.
You currently have $10 in your bank account.
Enter the amount of money that you would like to withdraw: -100
Removing $-100 from your account.
You currently have $110 in your bank account.
Enter the amount of money that you would like to withdraw: -1000000
Removing $-1000000 from your account.
You currently have $1000110 in your bank account.
Congratulations! You're rich!
```
The lack of bounds checking allows us to input a negative value and end up with a greater amount of money in our bank account. The cause of this issue is on line 18 of the code, where we have `money -= withdraw`. If we make `withdraw` a negative value, then `money` will be subtracting a negative value, which is the same thing as adding a positive value. If the programmer wanted to avoid this issue, then he should have made sure that `withdraw` is a positive integer.
Another way that this program could be exploited is by using an input value that is greater than the amount of money in our bank account. Zero is the lower bound of `money`, so if we try to subtract one more dollar after when `money` equals zero, `money` should get set equal to its upper bound.
```bash
$ ./vuln_bank
Welcome to Vuln Bank!
Your goal is to become a millionaire.
You currently have $10 in your bank account.
Enter the amount of money that you would like to withdraw: 10
Removing $10 from your account.
You currently have $0 in your bank account.
Enter the amount of money that you would like to withdraw: 1
Removing $1 from your account.
You currently have $4294967295 in your bank account.
Congratulations! You're rich!
```
In CTFs, it is common to see binaries where there are mathematical issues such as the ones shown above. You should keep this in mind whenever you're solving a CTF challenge that involves some kind of math, especially if both signed and unsigned numbers are being used. There are tools out there such as [Z3 Theorem Prover](https://wiki.bi0s.in/reversing/analysis/dynamic/linux/z3/) that can help you find mathematical issues like integer overflows.

## More Resources:
- [Two's Complement](https://www.tutorialspoint.com/two-s-complement)
- [Integer Limits](https://nickolasteixeira.medium.com/how-to-explain-to-my-wife-what-i-do-how-do-you-get-the-maximum-and-minimum-values-for-integer-befdc263a3a2)
- [Integer Overflow Examples](https://guyinatuxedo.github.io/35-integer_exploitation/index.html)

## Creators

**Nihaal Prasad**

Enjoy :metal:

<!--
<br><br>
Note: to upload screenshots/images, put them in the *images* directory and access them like so:<br>
`<p align="left"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/goat.jpg" width=50%  height=50%></p>`
<br>or, quicker, but with less adjustability:<br>
`![](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/goat.jpg)`
-->
