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
