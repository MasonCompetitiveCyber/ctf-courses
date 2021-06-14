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
