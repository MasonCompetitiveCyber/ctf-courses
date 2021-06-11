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
