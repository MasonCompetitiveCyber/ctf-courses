#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char buf[100];

    printf("Enter data plz: ");
    fgets(buf, 1000, stdin);

    return 0;
}
