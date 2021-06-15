#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char name[300];

    printf("Hello there!\n");
    printf("The buffer is at %p.\n", name);
    printf("Please enter your name: ");
    gets(name);

    return 0;
}
