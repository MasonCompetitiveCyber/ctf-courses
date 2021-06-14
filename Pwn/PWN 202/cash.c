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
