#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    char buf[100];
    
    while(strncmp("quit", buf, 4) != 0) {
        fgets(buf, 1000, stdin);
        printf(buf);
    }

    return 0;
}
