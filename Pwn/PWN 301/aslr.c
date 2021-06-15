#include <stdio.h>
#include <stdlib.h>

void vulns(char buf[50]) {
    printf("Format string vuln: ");
    fgets(buf, 50, stdin);
    printf(buf);
    printf("Buffer overflow: ");
    fgets(buf, 500, stdin);
}

int main(int argc, char **argv) {
    char buf[50];
    vulns(buf);
    return 0;
}
