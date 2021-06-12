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
