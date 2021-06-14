#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    printf("%3$d, %d", 1, 2, 3, 4, 5);
    return 0;
}
