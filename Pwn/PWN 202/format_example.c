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
